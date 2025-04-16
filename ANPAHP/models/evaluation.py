from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from .criterion import Criterion
from .objective import Objective
from .kpi import KPI
from .enumerations import UserType, UserDomain


NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 255
NB_OF_STEPS = 8 # The number of steps currently present in the process.


class Evaluation(models.Model):
    """Model representing an AHP-ANP Evaluation in our DB."""
    # User-provided information
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
    # if current_step == 3, then the first 2 steps have been completed,
    # and the user needs to complete the 3rd step before going further.
    current_step = models.IntegerField(default = 1)
    
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
    
    # action = models.TextField(blank = True, default = "")
    # ANPAHP_recommendations = models.TextField(blank=True, default = "")
    
    ############### these are exclusive for the KPIs.
    # KPIs = models.ManyToManyField(KPI)
    # selected_KPIs = models.TextField(default = "[]") #list of booleans
    
    # financial_scores = models.JSONField(default = dict)
    # financial_inconcistency = models.TextField(default = "[]")
    # financial_vector = models.JSONField(default = dict)
    # internal_processes_scores = models.JSONField(default = dict)
    # internal_processes_inconcistency = models.TextField(default = "[]")
    # internal_processes_vector = models.JSONField(default = dict)
    # learn_growth_scores = models.JSONField(default = dict)
    # learn_growth_inconcistency = models.TextField(default = "[]")
    # learn_growth_vector = models.JSONField(default = dict)
    # clients_scores = models.JSONField(default = dict)
    # clients_inconcistency = models.TextField(default = "[]")
    # clients_vector = models.JSONField(default = dict)
    
    # pairwise_combinations = models.JSONField(default = dict) # key = tuple (index, index), value = user defined score
    # KPIs_selected_names = models.TextField(default = "[]") # list of names
    

    
    ################# Criterion
    # BSC_Weights = models.TextField(default = "[]")
    # criteria = models.ManyToManyField(Criterion)
    # selected_criteria = models.TextField(default = "[]")
    # criteria_scores = models.JSONField(default = dict)
    # criteria_inconcistency = models.TextField(default = "[]")
    # criteria_vector = models.JSONField(default = dict)
    # pairwise_combinations_criteria = models.JSONField(default = dict)
    # criteria_selected_names = models.TextField(default = "[]")
    
    ############### RESULTS
    # shapes = models.TextField(default = '{"Objectives":1, "Criterions":0,"KPIs":0, "BSC":4}') # Sizes of the subdomain of the supermatrix
    # matrix_data = models.JSONField(default = dict) # The 4 matrics (bsc families)
    # matrix_data_pre = models.TextField(default = "[]")
    # results = models.TextField(default = "[]") 
    # hierarcy = models.TextField(default = "[]") # list of weights for metrics
    # supermatrix = models.TextField(default = "[]") # Matrix of the 4 bsc families matrices
    # rows = models.TextField(default = "[]")
    
    # ############## these are for the risk register ################################
    # # general comments
    # comments = models.TextField(default = "") # Comments by user
    # message = models.TextField(default = "") # Error message displayed in HTML
    # ##################################
    
    
    def save(self,*args,**kwargs):
        """Allows to automatically recompute the completion 'percentage'."""
        self.percentage = str(int(100 * (self.current_step - 1) / NB_OF_STEPS)) + "%"
        super(Evaluation, self).save(*args, **kwargs)
        
        
    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.title