"""Tests for module 'models.bsc_family.'"""

from django.core.exceptions import ValidationError
from django.test import TestCase

from ...models.bsc_family import (BSCFamily, 
                                  BSCSubfamily,
                                  NAME_MIN_LENGTH,
                                  NAME_MAX_LENGTH,
                                  SHORT_NAME_MIN_LENGTH,
                                  SHORT_NAME_MAX_LENGTH)


class BSCFamilyModelTests(TestCase):
    """Class to test model 'BSCFamily' in the ANPAHP app."""
    # TODO
    
    
class BSCSubfamilyModelTests(TestCase):
    """Class to test model 'BSCSubfamily' in the ANPAHP app."""
    # TODO