from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator

from .bsc_family import BSCSubfamily
from . import validators

NAME_MIN_LENGTH = 1


class KPI(models.Model):
    """Model representing KPIs in our DB."""
    # User-provided fields:
    name = models.TextField(primary_key = True, unique = True, 
                            validators=[MinLengthValidator(NAME_MIN_LENGTH)])
    alternative_names = models.JSONField(default = list, blank = True)
    bsc_subfamilies = models.ManyToManyField(BSCSubfamily)
    short_definition = models.TextField(default = "", blank = True)
    explanation = models.TextField(default = "", blank = True)
    
    # Automatically set fields:
    author = models.ForeignKey(User, on_delete = models.CASCADE, null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True, editable = False)
    last_updated = models.DateTimeField(auto_now = True)
    
    
    def get_bsc_families(self):
        """Gets the list of BSC families to which the KPI is associated.
        
        Return:
            list[BSCFamily] - The list of BSC families to which the KPI is associated.
        """
        return [sub.bsc_family for sub in self.bsc_subfamilies.all()]
    
    
    def shares_same_family(self, other_kpi):
        """Checks that the current KPI and the provided one share at least 1 BSC family.
        
        Args:
            other_kpi (KPI): The KPI to check for.
            
        Returns:
            bool - `True` if the two KPIs share at least 1 BSC family, `False` otherwise.
        """
        return bool(set(self.get_bsc_families()) & set(other_kpi.get_bsc_families()))

    
    def save(self, *args, **kwargs):
        """Overrides 'save()' to run all the validators on all the fields when saved."""
        validators.run_validators(self)
        self.full_clean() # See: https://docs.djangoproject.com/en/5.1/ref/models/instances/#django.db.models.Model.full_clean
        super(KPI, self).save(*args, **kwargs)


    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name
    
    
    @staticmethod
    def share_a_family(kpi1, kpi2):
        """Checks if the two provided KPIs share at least 1 BSC Family.
        
        Args:
            kpi1 (KPI): The first KPI to check.
            kpI2 (KPI): The second KPI to check.
            
        Returns:
            bool - `True` if the two KPIs share at least 1 BSC family,
            `False` otherwise.
        """
        return kpi1.shares_same_family(kpi2)