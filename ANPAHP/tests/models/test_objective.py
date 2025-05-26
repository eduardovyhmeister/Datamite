from datetime import timedelta
import time

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from ...models.objective import Objective, NAME_MIN_LENGTH


class ObjectiveModelTests(TestCase):
    """Class to test model 'Objective' in the ANPAHP app."""
    
    
    # def test_objective_valid_basic_creation(self):
    #     """An objective can be created and saved into the DB with just a name
    #     and the 'created' and 'last_updated' fields should be updated automatically."""
    #     new_objective = Objective(name = "Test")
    #     new_objective.save()
        
    #     objectives = Objective.objects.all()
    #     self.assertEqual(len(objectives), 1)
    #     self.assertEqual(objectives[0].name, "Test")
    #     self.assertEqual(objectives[0].explanation, "") # Should be the default value
    #     self.assertEqual(objectives[0].author, None) # Should be the default value
    #     self.assertLess(objectives[0].last_updated, timezone.now())
    #     self.assertGreater(objectives[0].last_updated, timezone.now() - timedelta(seconds = 0.1))
    #     creation_time = timezone.now()
    #     self.assertLess(objectives[0].created, creation_time)
        
    #     time.sleep(0.3)
        
    #     # Modify it and check that the last_update field is updated accordingly:
    #     new_objective.name = "NewName"
    #     new_objective.save()
        
    #     objectives = Objective.objects.all()
    #     self.assertEqual(len(objectives), 1)
    #     self.assertEqual(objectives[0].name, "NewName")
    #     self.assertLess(objectives[0].last_updated, timezone.now())
    #     self.assertGreater(objectives[0].last_updated, timezone.now() - timedelta(seconds = 0.1))
    #     self.assertLess(objectives[0].created, creation_time)


    # def test_objective_invalid_basic_creation(self):
    #     """An objective name must of at least NAME_MIN_LENGTH chars.
    #     Should raise a ValidationError if it's not."""
    #     new_objective = Objective(name = "a"*(NAME_MIN_LENGTH - 1))
    #     with self.assertRaises(ValidationError):
    #         new_objective.save()

    #     objectives = Objective.objects.all()
    #     self.assertEqual(len(objectives), 0)


    # def test_objective_valid_creation_with_user(self):
    #     """An objective can be associated to a user."""
    #     new_user = User(username = "Test Name", password = "Test Password")
    #     new_user.save()
        
    #     new_objective = Objective(name = "Test", author = new_user)
    #     new_objective.save()
        
    #     objectives = Objective.objects.all()
    #     self.assertEqual(len(objectives), 1)
    #     self.assertEqual(objectives[0].author, new_user)
        

    # def test_objective_duplicate(self):
    #     """Each objective name needs to be unique. Trying to save a
    #     duplicate should raise an exception."""
    #     new_objective = Objective(name = "Test")
    #     new_objective.save()
        
    #     new_objective2 = Objective(name = "Test", explanation = "blabla")
    #     with self.assertRaises(Exception):
    #         new_objective2.save()
            
    #     objectives = Objective.objects.all()
    #     self.assertEqual(len(objectives), 1)
    #     self.assertEqual(objectives[0].explanation, "")