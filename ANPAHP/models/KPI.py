from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from .enumerations import BSCFamily

class KPI(models.Model):
    """Models representing KPIs in our DB."""
    name = models.TextField(unique = True)
    explanation = models.TextField()
    BSCfamily = models.CharField(max_length = 100, choices = BSCFamily)
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    last_updated = models.DateTimeField(auto_now_add = True)
    
    def save(self, *args, **kwargs):
        """Allows to automatically save the last modified field."""
        self.last_updated = timezone.now()
        super(KPI, self).save(*args, **kwargs)

    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name