from datetime import timedelta
import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ...models.criterion import Criterion, NAME_MIN_LENGTH


class CriterionModelTests(TestCase):
    """Class to test model 'Criterion' in ANPAHP app."""
    
    
    def test_valid_basic_creation(self):
        """A Criterion can be created and saved into the DB with just a name
        and the 'created' and 'last_updated' fields should be updated automatically."""
        new_criterion = Criterion(name = "Test")
        new_criterion.save()
        
        criteria = Criterion.objects.all()
        self.assertEqual(len(criteria), 1)
        self.assertEqual(criteria[0].name, "Test")
        self.assertEqual(criteria[0].explanation, "") # Should be the default value
        self.assertEqual(criteria[0].author, None) # Should be the default value
        self.assertEqual(criteria[0].option, "") # Should be the default value
        self.assertLess(criteria[0].last_updated, timezone.now())
        self.assertGreater(criteria[0].last_updated, timezone.now() - timedelta(seconds = 0.1))
        creation_time = timezone.now()
        self.assertLess(criteria[0].created, creation_time)
        
        time.sleep(0.3)
        
        new_criterion.name = "NewName"
        new_criterion.save()
        
        criteria = Criterion.objects.all()
        self.assertEqual(len(criteria), 1)
        self.assertEqual(criteria[0].name, "NewName")
        self.assertLess(criteria[0].last_updated, timezone.now())
        self.assertGreater(criteria[0].last_updated, timezone.now() - timedelta(seconds = 0.1))
        self.assertLess(criteria[0].created, creation_time)
        
    
    def test_criterion_invalid_basic_creation(self):
        """A criterion name must have at least NAME_MIN_LENGTH chars.
        Should raise a ValidationError if it's not."""
        new_criterion = Criterion(name = "a"*(NAME_MIN_LENGTH - 1))
        with self.assertRaises(ValidationError):
            new_criterion.save()
           
        criteria = Criterion.objects.all()
        self.assertEqual(len(criteria), 0)
        
    
    def test_criterion_valid_creation_with_user(self):
        """A criterion can be associated to a user."""
        new_user = User(username = "Test Name", password = "Test Password")
        new_user.save()
        
        new_criterion = Criterion(name = "Test", author = new_user)
        new_criterion.save()
        
        criteria = Criterion.objects.all()
        self.assertEqual(len(criteria), 1)
        self.assertEqual(criteria[0].author, new_user)
        
        
    def test_criterion_duplicate(self):
        """Each criterion's name needs to be unique. Trying to save a criterion
        with already existing name should raise an exception."""
        new_criterion = Criterion(name = "Test")
        new_criterion.save()
        
        new_criterion2 = Criterion(name = "Test", explanation = "blabla")
        with self.assertRaises(Exception):
            new_criterion2.save()
            
        criteria = Criterion.objects.all()
        self.assertEqual(len(criteria), 1)
        self.assertEqual(criteria[0].explanation, "")
        
        
    def test_criterion_invalid_option(self):
        """An option can be provided on criteria. Should fail if something
        unexpected is provided."""
        new_criterion = Criterion(name = "Test", option = "fsdfjdsuf")
        with self.assertRaises(Exception):
            new_criterion.save()
            
        criteria = Criterion.objects.all()
        self.assertEqual(len(criteria), 0)