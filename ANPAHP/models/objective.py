from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .enumerations import UserType


class Objective(models.Model):
    """Model representing an objective in our DB."""
    name = models.TextField(unique = True)
    explanation = models.TextField()
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    last_updated = models.DateField(auto_now_add = True)
    
    def save(self, *args, **kwargs):
        """Allows to automatically save the last modified field."""
        self.last_updated = timezone.now()
        super(Objective, self).save(*args, **kwargs)

    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name