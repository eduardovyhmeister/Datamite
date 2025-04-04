from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator

from .enumerations import BSCFamily
from .validators import run_validators


NAME_MIN_LENGTH = 1


class KPI(models.Model):
    """Models representing KPIs in our DB."""
    name = models.TextField(unique = True, validators=[MinLengthValidator(NAME_MIN_LENGTH)])
    explanation = models.TextField(default = "", blank = True)
    BSCfamily = models.CharField(max_length = 100, choices = BSCFamily, null = False, blank = False)
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True, editable = False)
    last_updated = models.DateTimeField(auto_now = True)
    
    
    def save(self, *args, **kwargs):
        """Overrides 'save()' to run all the validators on all the fields when saved."""
        run_validators(self)
        self.full_clean() # See: https://docs.djangoproject.com/en/5.1/ref/models/instances/#django.db.models.Model.full_clean
        super(KPI, self).save(*args, **kwargs)


    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name