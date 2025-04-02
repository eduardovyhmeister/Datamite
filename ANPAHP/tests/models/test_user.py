from django.test import TestCase

from ...models.user import User


class UserModelTests(TestCase):
    """Class to test model 'User' in the ANPAHP app."""
    
    def test_max_first_name_length(self):
        """The 'first_name' field has a maximum length of 120 chars.
        It should fail if we try to insert something larger."""
        pass