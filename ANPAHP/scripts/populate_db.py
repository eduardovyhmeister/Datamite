"""Script used to populate the DB with the DATAMITE KPIs, criteria, and objectives.
To run this script, use the 'python manage.py runscript populate_db' while inside the
project folder. This scripts provide human-readable logs to let you know if anything
went wrong."""

import csv

from ANPAHP.models import KPI, Criterion, Objective, enumerations
import utils.custom_logger as logging


# Instantiate the logger for this script:
logger = logging.get_logger(__name__)


# Paths to the CSV files containing the information about
# KPIs, objectives and criteria.
KPIS_CSV_PATH = "static/mine/KPIs.csv"
OBJECTIVES_CSV_PATH = "static/mine/Objectives.csv"
CRITERIA_CSV_PATH = "static/mine/Criteria.csv"


def populate_KPIs():
    """Loads all of the KPIs defined in the Datamite project into the DB.
    Also checks for duplicated definitions and wrong BSCfamily values;
    will notify if it finds any issue."""
    file_name = KPIS_CSV_PATH
    logger.info(f"Loading the KPIs from '{file_name}'.")
    with open(file_name, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader) # Skips the header (stupid python module)
        names = []
        for i, row in enumerate(reader, start = 1):
            # Make sure the file is formatted correctly:
            try:
                name, explanation, BSCfamily = row
            except ValueError: # Happens when too few or too many values are provided.
                logger.critical(f"Invalid KPIs file - File '{file_name} should contain exactly three columns: 'name', 'explanation', and 'BSCfamily'.")
                return
            
            # Check for duplicate names within the same file:
            if name in names:
                logger.error(f"Duplicate KPI name - KPI '{name}' is defined multiple times in '{file_name}'.")
                continue
            names.append(name)
            
            # Check if the KPI already exists in the DB:
            if KPI.objects.filter(name = name).first():
                logger.warning(f"KPI '{name}' already existed in the DB.")
                continue
            
            # Check the validity of the BSCfamily value:
            if BSCfamily not in enumerations.BSCFamily:
                valid_values = [str(value) for value in enumerations.BSCFamily]
                logger.error(f"Unknown BSCfamily value - In file '{file_name}', line {i}, value '{BSCfamily}' is invalid, should be in {valid_values}")
                continue
                        
            kpi, created = KPI.objects.get_or_create(name = name, 
                                                     explanation = explanation, 
                                                     BSCfamily = BSCfamily)
            kpi.save()
            
            if created:
                logger.info(f"KPI '{name}' has been created in the DB.")
            else:
                logger.error(f"KPI '{name}' could not be created for some reason.")
    

def populate_objectives():
    """Loads all of the objectives defined in the Datamite project into the DB.
    Also checks for duplicated definitions and will notify if it finds any."""
    file_name = OBJECTIVES_CSV_PATH
    logger.info(f"Loading the objectives from '{file_name}'.")
    with open(file_name, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader) # Skips the header (stupid python module)
        names = []
        for row in reader:
            # Make sure the file is formatted correctly:
            try:
                name, explanation = row
            except ValueError:
                logger.critical(f"Invalid objectives file - File '{file_name} should contain exactly two columns: 'name', 'explanation'.")
                return
            
            # Check for duplicates within the same file:
            if name in names:
                logger.error(f"Duplicate objective name - Objective '{name}' is defined multiple times in '{file_name}'.")
                continue
            names.append(name)
            
            # Check if the objective already exists in the DB:
            if Objective.objects.filter(name = name).first():
                logger.warning(f"Objective '{name}' already existed in the DB.")
                continue
            
            # Create the objective:
            objective, created = Objective.objects.get_or_create(name = name, explanation = explanation)
            objective.save()
            
            if created:
                logger.info(f"Objective '{name}' has been created in the DB.")
            else:
                logger.error(f"Objective '{name}' could not be created for some reason.")
                

def populate_criteria():
    """Loads all the criteria defined in the Datamite project into the DB.
    Also checks for duplicated definitions and will notify if it finds any."""
    file_name = CRITERIA_CSV_PATH
    logger.info(f"Loading the criteria from '{file_name}'.")
    with open(file_name, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader) # Skips the header (stupid python module)
        names = []
        for row in reader:
            # Make sure the file is formatted correctly:
            try:
                name, explanation = row
            except ValueError:
                logger.critical(f"Invalid criteria file - File '{file_name} should contain exactly two columns: 'name', 'explanation'.")
                return
            
            # Check for duplicate names within the file:
            if name in names:
                logger.error(f"Duplicate criterion name - Criterion '{name}' is defined multiple times in '{file_name}'.")
                continue
            names.append(name)
            
            # Check if the criterion already exists in the DB:
            if Criterion.objects.filter(name = name).first():
                logger.warning(f"Criterion '{name}' already existed in the DB.")   
                continue
            
            criterion, created = Criterion.objects.get_or_create(name = name, explanation = explanation)
            criterion.save()
            
            if created:
                logger.info(f"Criterion '{name}' has been created in the DB.")
            else:
                logger.error(f"Criterion '{name}' could not be created for some reason.")


def run():
    """Function called by the 'python manage.py runscript' command."""
    populate_KPIs()
    populate_objectives()
    populate_criteria()