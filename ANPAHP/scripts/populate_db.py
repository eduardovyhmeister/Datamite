"""Script used to populate the DB with the DATAMITE KPIs, criteria, and objectives.
To run this script, use the 'python manage.py runscript populate_db' command while 
inside the project folder. This scripts provide human-readable logs to let you know 
if anything went wrong."""

import csv
import json
import os.path
import unicodedata
from typing import Type

import django.db.models
from django.core.exceptions import ObjectDoesNotExist, ValidationError

from ANPAHP.models import (BSCFamily,
                           BSCSubfamily,
                           KPI, 
                           Criterion, 
                           Objective)
import ANPAHP.models.helpers as model_helpers
import utils.custom_logger as logging


# Instantiate the logger for this script:
logger = logging.get_logger(__name__)


# Paths to the CSV files containing the data:
DATA_FOLDER = os.path.join("ANPAHP", "data")
BSC_FAMILIES_CSV_PATH = os.path.join(DATA_FOLDER, "BSC_families.csv")
BSC_SUBFAMILIES_CSV_PATH = os.path.join(DATA_FOLDER, "BSC_subfamilies.csv")
OBJECTIVES_CSV_PATH = os.path.join(DATA_FOLDER, "Objectives.csv")
CRITERIA_CSV_PATH = os.path.join(DATA_FOLDER, "Criteria.csv")
KPIS_CSV_PATH = os.path.join(DATA_FOLDER, "KPIs.csv")


# -----------------------------------------------------------------------------
# CSV header check functions:

def header_is_valid(header):
    """Checks that the header of a CSV is valid: only contains chars that can be
    used in a field's name (in this case chars that can be used in a Python variable
    name) and no duplicate names.
    
    Args:
        header (list[str]): The header to test.
        
    Returns:
        bool - 'True' if the header is valid, 'False' otherwise.
    """
    header_fields = set(header)
    if len(header_fields) != len(header):
        return False
    
    for field_name in header:
        if not field_name.isidentifier():
            return False
    
    return True


def header_unknown_fields(header: list[str], 
                          model_class: Type[django.db.models.Model]) -> list[str]:
    """Checks a header against a model and provides a list of fields appearing
    in the header but not in the model.
    
    Args:
        header (list[str]): The header of a CSV file.
        model (class): The model class to check against, must inherit from
            django.db.models.Model.
        
    Returns:
        list[str] - The list of unknown fields found in the CSV header.
    """
    all_fields = {field.name for field in model_helpers.get_custom_fields(model_class)}
    header_fields = set(header)
    if not header_fields.issubset(all_fields):
        return list(header_fields.difference(all_fields))
    return []


def header_missing_fields(header: list[str], 
                          model_class: Type[django.db.models.Model]) -> list[str]:
    """Checks a header against a model and provides a list of missing fields
    in the provided CSV header, required to create a record in the DB.
    
    Args:
        header (list[str]): The header of a CSV file.
        model_class (class): The model class to check against, must inherit
            from django.db.models.Model.
        
    Returns:
        list[str] - The list of required fields missing from the header.
    """
    header_fields = set(header)
    required_fields = {field.name for field in model_helpers.get_required_custom_fields(model_class)}
    
    if not required_fields.issubset(header_fields):
        return list(required_fields.difference(header_fields))
    return []
    
    
def check_csv_header(file_path: str, model_class: Type[django.db.models.Model]) -> bool:
    """Checks that the header of the provided CSV file matches the provided Model.
    If not, it will log a critical message and return 'False'.
    
    Args:
        file_path (str): The path to the CSV file to check.
        model_class (class): The model class to check against, must inherit
            from django.db.models.Model.
            
    Returns:
        bool - 'True' if the header is okay, 'False' otherwise.
    """
    with open(file_path, "r") as csv_file:
        reader = csv.reader(csv_file, quotechar = '"', delimiter = ',',
                            quoting = csv.QUOTE_ALL, skipinitialspace = True,
                            escapechar = "\\")
        header = [field_name.strip() for field_name in next(reader)]
        
        if not header_is_valid(header):
            logger.critical(f"Invalid CSV Header - File {file_path}'s header is invalid " + 
                            "(either duplicate column names or invalid column names).")
            return False
        
        if unknown_fields := header_unknown_fields(header, model_class):
            logger.critical(f"Invalid CSV Header Error - File {file_path}'s header is invalid, " +
                            f"some fields ({unknown_fields}) are unknown and do not correspond" +
                            f"to model {model_class}.")
            return False
        
        if missing_fields := header_missing_fields(header, model_class):
            logger.critical(f"Invalid CSV Header Error - File {file_path}'s header is invalid, " +
                            f"some required fields ({missing_fields} are missing to be able " +
                            f"to populate {model_class}.")
            return False
        
    return True


# -----------------------------------------------------------------------------
# Populate functions:

def populate_db(file_path: str, model_class: Type[django.db.models.Model]) -> None:
    """Loads all the record found in the provided CSV into the provided Model in the DB.
    Will perform checks on the header to make sure it makes sense compared to the model.
    Will also perform checks on fields (such as uniqueness) to make sure they are correct.
    Any record already found in the DB will be updated with the new data. If a record is
    not found in the DB, it is created.
    Will log messages to let you know if errors are found in the provided file.
    
    Args:
        file_path (str): The path to the file to load the BSC families from.
        model_class (class): The model class to check against, must inherit
            from django.db.models.Model.
    """
    logger.info(f"POPULATING MODEL '{model_class.__name__}' WITH DATA FROM '{file_path}':")
    if not check_csv_header(file_path, model_class): return
    
    with open(file_path, "r", encoding = "utf-8") as csv_file:
        reader = csv.reader(csv_file, quotechar = '"', delimiter = ',',
                            quoting = csv.QUOTE_ALL, skipinitialspace = True,
                            escapechar = "\\")
        header = [field_name.strip() for field_name in next(reader)]
        
        unique_fields = {field.name: set() for field in model_helpers.get_unique_custom_fields(model_class)}
        first_unique_field = model_helpers.get_unique_custom_fields(model_class)[0].name
        foreign_keys = {field.name: field for field in model_helpers.get_custom_foreign_keys(model_class)}
        many_to_many_fields = {field.name: field for field in model_helpers.get_custom_many_to_many_fields(model_class)}
        
        # Now process the data:
        for line_number, row in enumerate(reader, start = 2):
            row = [column.strip() for column in row]
            
            if len(row) != len(header):
                logger.error(f"Invalid Row Error - In file {file_path}, line {line_number} is invalid: " +
                             f"expected {len(header)} entries, got {len(row)} instead.")
                continue
            
            # Get the retrieval kwargs (in case the record already exist in the DB) and
            # get the creation kwargs if the record needs to be created:
            csv_kwargs = {field : value for field, value in zip(header, row)}
            creation_kwargs = {}      # Used for the creation of the record
            retrieval_kwargs = {}     # Used for retrieval of the existing record
            many_to_many_kwargs = {}  # Used for the many to many fields, that need to be set separately
            for field, value in csv_kwargs.items():
                # Retrieve foreign key's record from the DB:
                if field in foreign_keys:
                    try:
                        foreign_model = foreign_keys[field].remote_field.model
                        target_field = foreign_keys[field].target_field.name
                        creation_kwargs[field] = foreign_model.objects.get(**{target_field: value})
                    except ObjectDoesNotExist: # Could not find the foreign key!
                        logger.error(f"Invalid Row Error - In file {file_path}, line {line_number}, " +
                                     f"foreign key '{value}' does not exist in the DB, are you using the " +
                                     "correct field?")
                    continue
                    
                # Retrieve ManyToMany records from the DB:
                if field in many_to_many_fields:
                    try:
                        if value == "": # Empty value
                            value = []
                        elif "[" not in value: # Not a JSON list, just a single value
                            value = [value]
                        else: # A JSON list is provided:
                            value = json.loads(value)
                        m2m_foreign_model = many_to_many_fields[field].remote_field.model
                        m2m_target_field = many_to_many_fields[field].target_field.name
                        many_to_many_kwargs[field] = [m2m_foreign_model.objects.get(**{m2m_target_field: v})
                                                      for v in value]
                    except json.decoder.JSONDecodeError as e:
                        logger.error(f"Invalid JSON Format Error - In file {file_path}, line {line_number}, " +
                                     f"the ManyToManyField '{field}' was expecting a JSON list and raised the " +
                                     f"following exception: {e}")
                    except ObjectDoesNotExist: # Could not find at least one of the foreign keys
                        logger.error(f"Unknown Foreign Key Error - In file {file_path}, line {line_number}, " +
                                     f"the ManyToManyField '{field}' was provided an unknown foreign key, " +
                                     f"pls check that it contains only existing values: '{value}'.")
                    continue
                                
                # Type cast into the right value if you want something
                # other than text and/or many to many fields or foreign keys:
                # TODO
                
                # Handle uniqueness:
                if field in unique_fields and value in unique_fields[field]:
                    logger.error(f"Duplicate Unique Field Error - In file {file_path}, line {line_number}, " +
                                 f"value '{value}' already exists within the same file but field " +
                                 f"'{field}' has to have a unique value.")
                    continue
                if field in unique_fields:
                    retrieval_kwargs[field] = value
                    unique_fields[field].update(value)
                    
                creation_kwargs[field] = value
            
            # Update the record if it already exists in the DB:
            # (cannot retrieve something that doesn't have at least one unique value)
            if len(retrieval_kwargs) != 0:
                try:
                    record = model_class.objects.get(**retrieval_kwargs)
                    for field, value in creation_kwargs.items():
                        setattr(record, field, value)
                    record.save()
                    # Set the ManyToManyFields
                    for field_name, value in many_to_many_kwargs.items():
                        field = getattr(record, field_name)
                        field.set(value)
                    record.save()
                    logger.info(f"{model_class.__name__} '{creation_kwargs[first_unique_field]}' has been successfully updated.")
                    continue # Has been updated, proceed.
                except ValidationError as e:
                    logger.error(f"Invalid Row Error - In file {file_path}, line {line_number}, " +
                                 f"could not update record '{first_unique_field}' because " +
                                 f"the following ValidationError was raised: {e}")
                    return
                except ObjectDoesNotExist: pass # Will create the record instead
                
            # Not updated so create the record:
            try:
                record = model_class(**creation_kwargs)
                record.save()
                # Set the ManyToManyFields:
                for field_name, value in many_to_many_kwargs.items():
                    field = getattr(record, field_name)
                    field.set(value)
                record.save()
                logger.info(f"{model_class.__name__} '{creation_kwargs[first_unique_field]}' has been successfully created.")
            except ValidationError as e:
                logger.error(f"Invalid Row Error - In file {file_path}, line {line_number}, " +
                             f"could not create record '{creation_kwargs[first_unique_field]}' because " +
                             f"the following ValidationError was raised: {e}")


def run():
    """Function called by the 'python manage.py runscript' command."""
    populate_db(BSC_FAMILIES_CSV_PATH, BSCFamily)
    populate_db(BSC_SUBFAMILIES_CSV_PATH, BSCSubfamily)
    populate_db(OBJECTIVES_CSV_PATH, Objective)
    populate_db(CRITERIA_CSV_PATH, Criterion)
    populate_db(KPIS_CSV_PATH, KPI)