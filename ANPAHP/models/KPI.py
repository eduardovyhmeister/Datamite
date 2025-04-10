from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator

from .bsc_family import BSCSubfamily
from . import validators

NAME_MIN_LENGTH = 1


class KPI(models.Model):
    """Model representing KPIs in our DB."""
    name = models.TextField(primary_key = True, unique = True, 
                            validators=[MinLengthValidator(NAME_MIN_LENGTH)])
    alternative_names = models.JSONField(default = list)
    bsc_subfamilies = models.ManyToManyField(BSCSubfamily)
    short_definition = models.TextField(default = "", blank = True)
    explanation = models.TextField(default = "", blank = True)
    
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True, editable = False)
    last_updated = models.DateTimeField(auto_now = True)
    
    
    def save(self, *args, **kwargs):
        """Overrides 'save()' to run all the validators on all the fields when saved."""
        validators.run_validators(self)
        self.full_clean() # See: https://docs.djangoproject.com/en/5.1/ref/models/instances/#django.db.models.Model.full_clean
        super(KPI, self).save(*args, **kwargs)


    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name