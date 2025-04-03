from django.contrib.auth.models import User
from django.db import models

from django.core.validators import MinLengthValidator

from .validators import run_validators

NAME_MIN_LENGTH = 1

class Objective(models.Model):
    """Model representing an objective in our DB."""
    name = models.TextField(unique = True, validators=[MinLengthValidator(NAME_MIN_LENGTH)])
    explanation = models.TextField(default = "")
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    last_updated = models.DateTimeField(auto_now = True)
    
    def save(self, *args, **kwargs):
        """Overrides 'save()' to run all the validators on all the fields when saved."""
        run_validators(self)
        super(Objective, self).save(*args, **kwargs)

    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name
    