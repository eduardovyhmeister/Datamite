"""
Custom validator functions for our custom models. Also contains
'run_validators()' used to make sure to run all the validators whenever
you want (e.g. in 'save()' right before saving).
"""


from django.core.exceptions import ValidationError
from django.db.models import Model
from django.forms.models import model_to_dict


# -----------------------------------------------------------------------------
# Helpers:

def run_validators(instance: Model) -> None:
    """Runs all the validators for all the fields in the model.
    Can be used in the override of the 'save()' method of a model
    to make sure every field is validated before saving.
    
    Args:
        instance (django.models.Model) - The instance of a model 
            for which you wish to run the validators.
    
    Raises:
        django.core.exceptions.ValidationError - If any of the validators fail.
    """
    # For every field in the model:
    for field_name, field_value in model_to_dict(instance).items():
        
        # Find the validators:
        model_field = getattr(instance.__class__, field_name)
        field = getattr(model_field, 'field', object())
        validators = getattr(field, 'validators', list())
        
        # Run the validators:
        for validator_func in validators:
            if field_value is not None:
                validator_func(field_value)
                

# -----------------------------------------------------------------------------
# Validators:

