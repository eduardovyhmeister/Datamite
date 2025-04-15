from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.core.validators import MinLengthValidator, MaxLengthValidator

from .validators import run_validators


NAME_MIN_LENGTH, NAME_MAX_LENGTH = 1, 255
SHORT_NAME_MIN_LENGTH, SHORT_NAME_MAX_LENGTH = 1, 64


# -----------------------------------------------------------------------------


class BSCFamily(models.Model):
    """Model representing BSC families in our DB (especially for content and
    the knowledge base)."""
    # TODO: check that the slugify name is unique too.
    name = models.CharField(primary_key = True, unique = True, blank = False, 
                            null = False, max_length = NAME_MAX_LENGTH,
                            validators = [MinLengthValidator(NAME_MIN_LENGTH),
                                          MaxLengthValidator(NAME_MAX_LENGTH)])
    short_name = models.CharField(unique = True, blank = False,
                                  null = False, max_length = SHORT_NAME_MAX_LENGTH,
                                  validators = [MinLengthValidator(SHORT_NAME_MIN_LENGTH),
                                                MaxLengthValidator(SHORT_NAME_MAX_LENGTH)])
    short_definition = models.TextField(blank = False, null = False)
    explanation = models.TextField(blank = False, null = False)
    
    
    def save(self, *args, **kwargs):
        """Overrides 'save()' to run all the validators on all the fields when saved."""
        run_validators(self)
        self.full_clean() # See: https://docs.djangoproject.com/en/5.1/ref/models/instances/#django.db.models.Model.full_clean
        super(BSCFamily, self).save(*args, **kwargs)


    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name
    
    
    @staticmethod
    def get_family_choices():
        """Provides the list of choices in terms of BSCFamily
        for the forms requiring to specify a BSCFamily.
        
        Returns:
            list(tuple(str, str)) - A list of choices in the 
            form of '(value, text_to_show)'.
        """
        return [(family.short_name, family.name) for family in BSCFamily.objects.all()]
    
        
    @staticmethod
    def is_in_choices(value):
        """Tests if the provided value is a valid value that can be selected
        as a choice of BSCFamily.
        
        Args:
            value (str): The string to test.
            
        Returns:
            bool - 'True' if the value is valid, 'False' otherwise.
        """
        return value in [subfamily.name for subfamily in BSCSubfamily.objects.all()]
    
    
# -----------------------------------------------------------------------------
    
    
class BSCSubfamily(models.Model):
    """Model representing the subcategories of the BSCFamilies in our DB 
    (especially for content and the knowledge base)."""
    # TODO: check that the slugify name is unique too.
    name = models.CharField(primary_key = True, unique = True, blank = False, 
                            null = False, max_length = NAME_MAX_LENGTH,
                            validators = [MinLengthValidator(NAME_MIN_LENGTH),
                                          MaxLengthValidator(NAME_MAX_LENGTH)])
    bsc_family = models.ForeignKey(BSCFamily, to_field = "name",
                                   on_delete = models.CASCADE, 
                                   null = False, blank = False)
    short_definition = models.TextField(blank = False, null = False)
    explanation = models.TextField(blank = False, null = False)
    

    def save(self, *args, **kwargs):
        """Overrides 'save()' to run all the validators on all the fields when saved."""
        run_validators(self)
        self.full_clean() # See: https://docs.djangoproject.com/en/5.1/ref/models/instances/#django.db.models.Model.full_clean
        super(BSCSubfamily, self).save(*args, **kwargs)


    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.name
    
    
    @staticmethod
    def get_subfamily_choices():
        """Provides the list of choices in terms of BSCFamily + BSC subfamily
        for the forms requiring to specify a subfamily.
        
        Returns:
            list(tuple(str, str)) - A list of choices in the 
            form of '(value, text_to_show)'.
        """
        return [(subfamily.name, 
                 f"{subfamily.bsc_family.name} - {subfamily.name}")
                for subfamily in BSCSubfamily.objects.all()]
        
    
    @staticmethod
    def is_in_choices(value):
        """Tests if the provided value is a valid value that can be selected
        as a choice of BSCSubfamily.
        
        Args:
            value (str): The string to test.
            
        Returns:
            bool - 'True' if the value is valid, 'False' otherwise.
        """
        return value in [subfamily.name for subfamily in BSCSubfamily.objects.all()]