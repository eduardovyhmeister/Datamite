from django.test import TestCase
from django.core.exceptions import ValidationError

from ...models import user


class UserModelTests(TestCase):
    """Class to test model 'User' in the ANPAHP app."""
    
    
    def test_user_creation_correct(self):
        """A User can be created and saved into the DB."""
        new_user = user.User(first_name = "test", 
                        last_name = "last_test", 
                        email_address = "test@tests.com")
        new_user.save()
        
        users = user.User.objects.all()
        self.assertEqual(len(users), 1)
        self.assertEqual(users[0].first_name, "test")
        self.assertEqual(users[0].last_name, "last_test")
        self.assertEqual(users[0].email_address, "test@tests.com")
    
    
    def test_max_first_name_length(self):
        """The 'first_name' field has a maximum length of NAME_MAX_LENGTH chars.
        It should fail if we try to insert something larger."""
        new_user = user.User(first_name = "a"*(user.NAME_MAX_LENGTH + 1),
                             last_name = "b" * (user.NAME_MAX_LENGTH),
                             email_address = "test@tests.com")

        with self.assertRaises(ValidationError):
            new_user.save()
        
        users = user.User.objects.all()
        self.assertEqual(len(users), 0)
        
        
    def test_min_first_name_length(self):
        """The 'first_name' field has a minimum length of NAME_MIN_LENGTH chars.
        It should fail if we try to insert something smaller."""
        new_user = user.User(first_name = "",
                             last_name = "test",
                             email_address = "test@tests.com")

        with self.assertRaises(ValidationError):
            new_user.save()
        
        users = user.User.objects.all()
        self.assertEqual(len(users), 0)
        
    
    def test_max_last_name_length(self):
        """The 'last_name' field has a maximum length of NAME_MAX_LENGTH chars.
        It should fail if we try to insert something larger."""
        new_user = user.User(first_name = "a"*(user.NAME_MAX_LENGTH),
                             last_name = "b" * (user.NAME_MAX_LENGTH + 1),
                             email_address = "test@tests.com")

        with self.assertRaises(ValidationError):
            new_user.save()
        
        users = user.User.objects.all()
        self.assertEqual(len(users), 0)
        
        
    def test_min_first_name_length(self):
        """The 'last_name' field has a minimum length of NAME_MIN_LENGTH chars.
        It should fail if we try to insert something smaller."""
        new_user = user.User(first_name = "test",
                             last_name = "",
                             email_address = "test@tests.com")

        with self.assertRaises(ValidationError):
            new_user.save()
        
        users = user.User.objects.all()
        self.assertEqual(len(users), 0)
    
    
    def test_invalid_email(self):
        """The field 'email_address' should be a valid email address.
        It should fail if we try to insert an invalid address."""
        new_user = user.User(first_name = "first_test",
                             last_name = "last_test",
                             email_address = "test@tests")
        with self.assertRaises(ValidationError) as e:
            new_user.save()
        users = user.User.objects.all()
        self.assertEqual(len(users), 0)
        
        new_user = user.User(first_name = "first_test",
                             last_name = "last_test",
                             email_address = "test@")
        with self.assertRaises(ValidationError) as e:
            new_user.save()
        users = user.User.objects.all()
        self.assertEqual(len(users), 0)
        
        new_user = user.User(first_name = "first_test",
                             last_name = "last_test",
                             email_address = "test.com")
        with self.assertRaises(ValidationError) as e:
            new_user.save()
        users = user.User.objects.all()
        self.assertEqual(len(users), 0)
        
        
    def test_duplicate_email(self):
        """The field 'email_address' has to be unique.
        It should fail when trying to add a new user with the same email address."""
        email_address = "tests@tests.com"
        new_user = user.User(first_name = "first_test",
                             last_name = "last_test",
                             email_address = email_address)
        new_user2 = user.User(first_name = "first_duplicate",
                              last_name = "last_duplicate",
                              email_address = email_address)
        new_user.save()
        with self.assertRaises(Exception): # The type of exception doesn't really matter
            new_user2.save()
            
    
    def test_duplicate_name(self):
        """As long as 'email_address' is unique, two users can have the same name."""
        first_name = "first_test"
        last_name = "last_name"
        new_user = user.User(first_name = first_name,
                             last_name = last_name,
                             email_address = "test@tests.com")
        new_user2 = user.User(first_name = first_name,
                              last_name = last_name,
                              email_address = "test2@tests.com")
        new_user.save()
        new_user2.save()