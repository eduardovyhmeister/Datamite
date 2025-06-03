"""Model for an AHP-ANP evaluation in our DB. In here, you can set the number
of steps currently present in the process (used to update the progression bar),
the fields to reset at each step when changes are detected, the default values
for the fields of the evaluation. 

If you plan on modifying this file, please make sure to read all the doc/comments
to not forget to update what needs to be updated and not break anything."""

from collections import defaultdict

from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from model_utils import FieldTracker # https://django-model-utils.readthedocs.io/en/latest/index.html

from .criterion import Criterion
from .objective import Objective
from .kpi import KPI
from .enumerations import UserType, UserDomain


NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 255
NB_OF_STEPS = 8 # The number of steps currently present in the process.

# To use in combination with tracker.has_changed(current_step).
# If you detect changes in some fields in certain steps, you need
# to reset to default values some of the fields. If you add fields
# to evaluation, or any new step, please update this. This is used
# to make sure there is consistency in the database and that any
# modification through a step is propagated nicely to the following
# steps.
# The format is simple: dict[step_number: list['field_names']].
FIELDS_TO_RESET = defaultdict(list,
{
    0: [],
    1: [],
    2: ['kpis', 'kpis_preferences', 'intermetric_relationships', 'intermetric_preferences'],
    3: ['kpis_preferences', 'intermetric_relationships', 'intermetric_preferences'],
    4: [],
    5: ['criteria_preferences'],
    6: [],
    7: ['intermetric_preferences'],
})
# Use this to set the default value to which the field will be reset
# to when a step change is detected. If a callable is provided (e.g. dict),
# then it will be called with no arguments.
# Format: dict[field_name: default_value or callable]
FIELDS_DEFAULT_VALUE = {
    'bsc_preferences': dict,
    'kpis': None, # Actually unnecessary since it's a ManyToManyField (.clear() is used instead)
    'kpis_preferences': dict,
    'criteria': None,
    'criteria_preferences': dict,
    'intermetric_relationships': None,
    'intermetric_preferences': None,
}


class Evaluation(models.Model):
    """Model representing an AHP-ANP Evaluation in our DB."""
    # User-provided information:
    name = models.CharField(unique = True, null = False, 
                            max_length = NAME_MAX_LENGTH,
                            validators = [MinLengthValidator(NAME_MIN_LENGTH),
                                          MaxLengthValidator(NAME_MAX_LENGTH)])
    notes = models.TextField(blank = True, default = "")
    user_type = models.CharField(max_length = 100, choices = UserType)
    user_domain = models.CharField(max_length = 100, choices = UserDomain)
    
    # Automatically assigned information:
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    created = models.DateTimeField(auto_now_add = True, editable = False)
    last_modified = models.DateTimeField(auto_now = True)
    percentage = models.TextField(default = r"0%") # completion percentage
    
    # The current step of the process the user is at for their evaluation.
    # Used to determine which steps should be shown or not, for example,
    # if current_step == 2, then the first 2 steps have been completed,
    # and the user needs to complete the 3rd step before going further.
    current_step = models.IntegerField(default = 0)
    
    # Step 1 - Select an objective:
    objective = models.ForeignKey(Objective, to_field = 'name', 
                                  on_delete = models.CASCADE,
                                  null = True)
    
    # Step 2 - BSC preferences:
    # Dict[BSCFamily.name: preference_value (0 to 100)]
    bsc_preferences = models.JSONField(default = dict)
    
    # Step 3 - KPIs selection:
    kpis = models.ManyToManyField(KPI)
    
    # Step 4 - KPIs preferences:
    # Dict[KPI.name: preference_value (1 to 100)]
    kpis_preferences = models.JSONField(default = dict)
    
    # Step 5 - Criteria selection:
    criteria = models.ManyToManyField(Criterion)
    
    # Step 6 - Criteria preferences:
    # Dict[Criterion.name: preference_value (1 to 100)]
    criteria_preferences = models.JSONField(default = dict)
    
    # Step 7 - Intermetric relationships:
    # Dict[KPI.name: list[KPI.name]]
    # Defaults to None to differentiate between an empty dict (which
    # is a valid input from the user) and the absence of value.
    intermetric_relationships = models.JSONField(default = None, null = True)
    
    # Step 8 - Intermetric relationships preferences:
    # Dict[KPI.name: Dict[KPI.name: preference_value (1 to 100)]]
    # If only 1 KPI influence has been selected, the default preference
    # value will be 100.
    # Defaults to None to differentiate between an empty dict (which
    # is a valid input from the user if there was no intermetric relationships)
    # and the absence of value.
    intermetric_preferences = models.JSONField(default = None, null = True)
    
    # Used to track changes in a field, prevents resetting the whole
    # Evaluation model when coming back to a previous step and clicking confirm
    # without having changed anything to the actual values submitted:
    tracker = FieldTracker()
    
    
    # action = models.TextField(blank = True, default = "")
    # ANPAHP_recommendations = models.TextField(blank=True, default = "")
    ############### RESULTS
    # shapes = models.TextField(default = '{"Objectives":1, "Criterions":0,"KPIs":0, "BSC":4}') # Sizes of the subdomain of the supermatrix
    # matrix_data = models.JSONField(default = dict) # The 4 matrics (bsc families)
    # matrix_data_pre = models.TextField(default = "[]")
    # results = models.TextField(default = "[]") 
    # hierarcy = models.TextField(default = "[]") # list of weights for metrics
    # supermatrix = models.TextField(default = "[]") # Matrix of the 4 bsc families matrices
    # rows = models.TextField(default = "[]")
    
    
    def save(self,*args,**kwargs):
        """Override 'save()' to enable an automatic reset of certain fields when
        going back to a previous step in the process. Also allows to automatically 
        recompute the completion 'percentage'."""
        # Track if the current_step has changed a reset fields as required:
        reset_m2m_fields = []
        if self.tracker.has_changed('current_step'):
            for field_name in FIELDS_TO_RESET[self.current_step]:
                field_object = self._meta.get_field(field_name)
            
                # Save ManyToManyFields' names for later reset:
                if isinstance(field_object, models.ManyToManyField):
                    reset_m2m_fields.append(field_name)
                    continue
                
                # Reset regular fields:
                default = FIELDS_DEFAULT_VALUE[field_name]
                setattr(self, field_name, default() if callable(default) else default)
                
        # Compute the completion percentage for the whole process:
        self.percentage = str(int(100 * (self.current_step) / NB_OF_STEPS)) + "%"
        
        # Effectively save:
        super(Evaluation, self).save(*args, **kwargs)
        
        # ManyToManyFields can only be reset after the model is saved for some reason:
        for field_name in reset_m2m_fields:
            getattr(self, field_name).set([])
            
        
    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.title