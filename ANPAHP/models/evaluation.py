from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from .criterion import Criterion
from .objective import Objective
from .KPI import KPI
from .enumerations import UserType, UserDomain


class Evaluation(models.Model):
    """Model representing an Evaluation in our DB."""
    # User information
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    notes = models.TextField(blank = True)
    ANPAHP_recommendations = models.TextField(blank=True, default = "")
    percentage = models.TextField(default = r"0%") # this is the % on how ready is the service
    publication_date = models.DateTimeField(auto_now_add = True)
    last_modified = models.DateTimeField(auto_now_add = True)
    action = models.TextField(blank = True, default = "")
    user_type = models.CharField(max_length = 100, choices = UserType)
    
    #Stages
    step_status1 = models.BooleanField(default = False)
    step_status2 = models.BooleanField(default = False)
    step_status3 = models.BooleanField(default = False)
    step_status4 = models.BooleanField(default = False)
    step_status5 = models.BooleanField(default = False)
    step_status6 = models.BooleanField(default = False)
    step_status7 = models.BooleanField(default = False)
    step_status8 = models.BooleanField(default = False)
    
    ############### these are exclusive for the KPIs.
    KPIs = models.ManyToManyField(KPI)
    selected_KPIs =  models.TextField(default = "[]")
    
    financial_scores = models.JSONField(default = dict)
    financial_inconcistency = models.TextField(default = "[]")
    financial_vector = models.JSONField(default = dict)
    internal_processes_scores = models.JSONField(default = dict)
    internal_processes_inconcistency = models.TextField(default = "[]")
    internal_processes_vector = models.JSONField(default = dict)
    learn_growth_scores = models.JSONField(default = dict)
    learn_growth_inconcistency = models.TextField(default = "[]")
    learn_growth_vector = models.JSONField(default = dict)
    clients_scores = models.JSONField(default = dict)
    clients_inconcistency = models.TextField(default = "[]")
    clients_vector = models.JSONField(default = dict)
    
    pairwise_combinations = models.JSONField(default = dict)
    KPIs_selected_names = models.TextField(default = "[]")
    
    ################# OBJECTIVES
    objectives = models.ManyToManyField(Objective)
    selected_objectives = models.TextField(default = "[]")
    objectives_scores = models.JSONField(default = dict)
    objectives_inconcistency = models.TextField(default = "[]")
    objectives_vector = models.JSONField(default = dict)
    pairwise_combinations_objectives = models.JSONField(default = dict)
    
    ################# Criterion
    BSC_Weights = models.TextField(default = "[]")
    criteria = models.ManyToManyField(Criterion)
    selected_criteria = models.TextField(default = "[]")
    criteria_scores = models.JSONField(default = dict)
    criteria_inconcistency = models.TextField(default = "[]")
    criteria_vector = models.JSONField(default = dict)
    pairwise_combinations_criteria = models.JSONField(default = dict)
    criteria_selected_names = models.TextField(default = "[]")
    
    ############### RESULTS
    shapes = models.TextField(default = "[]")
    matrix_data = models.JSONField(default = dict)
    matrix_data_pre = models.TextField(default = "[]")
    results = models.TextField(default = "[]")
    hierarcy = models.TextField(default = "[]")
    supermatrix = models.TextField(default = "[]")
    rows = models.TextField(default = "[]")
    
    ############## these are for the risk register ################################
    # general comments
    comments = models.TextField(default = "")
    message = models.TextField(default = "")
    ##################################
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
        self.last_modified = timezone.now()
        super(Evaluation, self).save(*args, **kwargs)
        
        
    def __str__(self):
        """Overrides the str() methods. Used for a human readable form of the model."""
        return self.title