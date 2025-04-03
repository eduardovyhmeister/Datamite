from django.db import models
from django.forms.models import model_to_dict
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator, MinLengthValidator

NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 120

class User(models.Model):
    """Model representing a user in our DB."""
    first_name = models.CharField('First Name', max_length = NAME_MAX_LENGTH, # Depends only on the DB
                                  validators = [MaxLengthValidator(NAME_MAX_LENGTH), 
                                                MinLengthValidator(NAME_MIN_LENGTH)])
    last_name = models.CharField('Last Name', max_length = NAME_MAX_LENGTH,
                                 validators = [MaxLengthValidator(NAME_MAX_LENGTH), 
                                               MinLengthValidator(NAME_MIN_LENGTH)])
    email_address = models.EmailField('User Email', unique = True)


    def run_validators(self):
        """Runs all the validators for all the fields in the model."""
        for field_name, field_value in model_to_dict(self).items():
            model_field = getattr(User, field_name)
            field = getattr(model_field, 'field', object())
            validators = getattr(field, 'validators', list())
            for validator_func in validators:
                if field_value is not None:
                    validator_func(field_value)


    def save(self, *args, **kwargs):
        """Overrides 'save()' enforcing validators whenever something is saved.
        
        Raises:
            django.core.exceptions.ValidationError - If any of the validators fail.
        """
        self.run_validators()
        super().save(*args, **kwargs)
    

    def __str__(self): 
        """Overrides the str() methods. Used for a human readable form of the model."""
        return f"{self.first_name} {self.last_name} ({self.email_address})"