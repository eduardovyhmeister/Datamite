from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .validators import run_validators

class Objective(models.Model):
    """Model representing an objective in our DB."""
    name = models.TextField(unique = True)
    explanation = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    last_updated = models.DateField(auto_now_add = True)
    
    def save(self, *args, **kwargs):
        """Overrides 'save()' to:
            - Allow to automatically save the last modified field.
            - Run all the validators on all the fields.    
        """
        self.last_updated = timezone.now()
        run_validators(self)
        super(Objective, self).save(*args, **kwargs)

    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name