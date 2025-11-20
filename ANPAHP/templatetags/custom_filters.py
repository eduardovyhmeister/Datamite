"""
Custom filters to be used in templates.
To make them available in your template, use '{% load custom_filters %}'
at the top of your template file.

For more information on custom tags and filters, see the Django doc here:
https://docs.djangoproject.com/en/5.1/howto/custom-template-tags/
"""

from django import template
from django.utils import text
register = template.Library()

import utils.environment as environment


@register.filter
def get_value_at(indexable, index_or_key):
    """Custom template filter to get the value at the specified index or key in an 
    indexable object (e.g. list or dict, i.e. any object that implements __get_item__()).
    Example of usage in a template:
    '{% my_list|get_value_at: index_number_or_key %}
    
    Args:
        indexable (indexable): The list to look into.
        index (int | immutable object): The index or key to get the value for.
        
    Returns:
        any - The value stored at the provided index/key. Returns 'None'
        if the index/key is incorrect or if the provided object isn't indexable.
    """
    try:
        return indexable[index_or_key]
    except (TypeError, IndexError, KeyError):
        return None


@register.filter
def slugify(string):
    """Slugifies a string to make it usable in JS and URLs.
    
    Args:
        string (str): The string to slugify.
        
    Returns:
        str - A slugified version of the string, compatible with URLs and JS.
    """
    return text.slugify(string)


@register.filter
def env(var_name):
    """Retrieve an environment variable from the environment utility.
    
    Args:
        var_name (str): The name of the variable to retrieve.
    
    Returns:
        Any - The value for that environment variable, `None` if
        not found.
    """
    try:
        environment.__dict__[var_name]
    except KeyError:
        return None