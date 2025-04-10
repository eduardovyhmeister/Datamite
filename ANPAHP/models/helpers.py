"""Helper functions for Django models and fields."""

from typing import Type
from collections.abc import Callable

from django.db.models import Field, Model, ForeignKey, ManyToManyField


def field_is_required(field: Field) -> bool:
    """Tests if the provided field is required when trying to save the model
    that contains it.
    
    Args:
        field (django.db.models.Field): The field to test.
    
    Returns:
        bool - 'True' if the field is mandatory, 'False' otherwise.
    """
    # TODO: might not work for every type of Field.
    return not field.null and (not field.blank or not field.default)


def get_custom_fields(model_class: Type[Model]) -> list[Field]:
    """Gets the list of all custom fields (fields you implemented yourself 
    in your model classes) from a 'Model'. Will not return any automatically
    created fields such 'ManyToOne' relationships or unique IDs.
    
    Args:
        model_class (class): The 'Model' to extract the fields, must inherit
            from django.db.models.Model.
        
    Returns:
        list[django.db.models.Field] - The list of custom fields for a model
        (i.e. the fields you implemented yourself in the class).
    """
    return [field for field in model_class._meta.get_fields(include_parents = False) 
            if not field.auto_created]


def get_required_custom_fields(model_class: Type[Model]) -> list[Field]:
    """Gets the list of all custom fields (fields you implemented yourself
    in your model classes) required when saving a 'Model'. Will not return 
    any automatically created fields such 'ManyToOne' relationships or unique IDs.
    
    Args:
        model_class (class): The 'Model' to extract the fields from, must inherit
            from django.db.models.Model.
        
    Returns:
        list[django.db.models.Field] - The list of custom fields required for a model
        (i.e. the fields you implemented yourself in the class).
    """
    return [field for field in get_custom_fields(model_class)
            if field_is_required(field)]
    
    
def get_unique_custom_fields(model_class: Type[Model]) -> list[Field]:
    """Gets the list of all custom fields (fields you implemented yourself
    in your model classes) that have to be unique in the DB. Will not return 
    any automatically created fields such 'ManyToOne' relationships or unique IDs.
    
    Args:
        model_class (class): The 'Model' to extract the fields from, must inherit
            from django.db.models.Model.
        
    Returns:
        list[django.db.models.Field] - The list of custom fields that have the
        'unique' attribute set to 'True'.
    """
    return [field for field in get_custom_fields(model_class)
            if field.unique]
    
    
def get_custom_foreign_keys(model_class: Type[Model]) -> list[Field]:
    """Gets the list of all custom fields (fields you implemented yourself
    in your model classes) that foreign keys. Will not return  any automatically 
    created fields such 'ManyToOne' relationships or unique IDs.
    
    Args:
        model_class (class): The 'Model' to extract the fields from, must inherit
            from django.db.models.Model.
            
    Returns:
        list[django.db.models.Field] - The list of foreign keys in the model.
    """
    return [field for field in get_custom_fields(model_class) if isinstance(field, ForeignKey)]
    

def get_custom_many_to_many_fields(model_class):
    """TODO"""
    return [field for field in get_custom_fields(model_class) if isinstance(field, ManyToManyField)]
    

def get_casting_function(field_class: type[Field]) -> Callable:
    """Returns the right casting callable (usually a function) to convert from text to the 
    required type for the field. If your field type doesn't seem to be supported here, this 
    is where to add it.

    Args:
        field_class:
    
    Returns:
        Callable - A callable used to perform type casting.
    """
    pass # TODO