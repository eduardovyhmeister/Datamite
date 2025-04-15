"""Module for helper functions used in the views."""

from django.utils import text


def slug_equal(str1, str2):
    """Check that the two provided strings have the same value once slugified.
    An already slugified string will keep the same value after being slugified 
    again.
    
    Args:
        str1 (str): The first string to compare.
        str2 (str): The second string to compare.
        
    Returns:
        bool - 'True' if the two strings are equal once slugified, 'False' otherwise.
    """
    return text.slugify(str1) == text.slugify(str2)



