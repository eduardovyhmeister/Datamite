"""Model representing a criterion in our DB."""


from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .enumerations import CriterionOption


class Criterion(models.Model):
    name = models.TextField(unique=True)
    explanation = models.TextField()
    option = models.CharField(max_length = 100, choices = CriterionOption)
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    last_updated = models.DateField(auto_now_add = True)
    
    def save(self, *args, **kwargs):
        """Allows to automatically save the last modified field."""
        self.updated = timezone.now()
        super(Criterion, self).save(*args, **kwargs)

    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name
