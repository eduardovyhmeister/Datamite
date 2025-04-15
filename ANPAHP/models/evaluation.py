from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models

from .criterion import Criterion
from .objective import Objective
from .kpi import KPI
from .enumerations import UserType, UserDomain


NAME_MIN_LENGTH = 1
NAME_MAX_LENGTH = 255


class Evaluation(models.Model):
    """Model representing an AHP-ANP Evaluation in our DB."""
    # User-provided information
    name = models.CharField(unique = True, null = False, 
                            max_length = NAME_MAX_LENGTH,
                            validators = [MinLengthValidator(NAME_MIN_LENGTH),
                                          MaxLengthValidator(NAME_MAX_LENGTH)])
    notes = models.TextField(blank = True, default = "")
    user_type = models.CharField(max_length = 100, choices = UserType)
    
    # Automatically assigned information:
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add = True, editable = False)
    last_modified = models.DateTimeField(auto_now = True)
    percentage = models.TextField(default = r"0%") # completion percentage
    
    #Stages
    step_status1 = models.BooleanField(default = False)
    step_status2 = models.BooleanField(default = False)
    step_status3 = models.BooleanField(default = False)
    step_status4 = models.BooleanField(default = False)
    step_status5 = models.BooleanField(default = False)
    step_status6 = models.BooleanField(default = False)
    step_status7 = models.BooleanField(default = False)
    step_status8 = models.BooleanField(default = False)
    
    # Step 1: Select an objective:
    objective = models.ForeignKey(Objective, to_field = 'name', 
                                  on_delete = models.CASCADE,
                                  null = True)
    
    
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
    user_domain = models.CharField(max_length = 100, choices = UserDomain)
    
    
    def save(self,*args,**kwargs):
        """Allows to automatically save the 'last_modified' field and recompute the completion 'percentage'."""
        self.percentage = str(int(100*(int(self.step_status1) + 
                                       int(self.step_status2) + 
                                       int(self.step_status3) + 
                                       int(self.step_status4) + 
                                       int(self.step_status5) + 
                                       int(self.step_status6) + 
                                       int(self.step_status7) + 
                                       int(self.step_status8))/8))+"%"
        super(Evaluation, self).save(*args, **kwargs)
        
        
    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.title