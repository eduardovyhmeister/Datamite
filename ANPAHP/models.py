from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
import datetime
from multiselectfield import MultiSelectField # this is installed from the app django-multiselectfield
import numpy as np
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone

# Create your models here.


class Users(models.Model):
    first_name = models.CharField('First Name', max_length=120)   #### this is text.
    last_name = models.CharField('Last Name', max_length=120)   #### this is text.
    email_address = models.EmailField('User Email',blank=False,unique=True)

    def __str__(self): # alows use our model in the admin area    outsi!!!!!!
        return self.first_name + ' ' + self.last_name

class KPI(models.Model):
    name = models.TextField(null=True,unique=True)
    explanation = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    updated = models.DateTimeField(auto_now_add=True)
    BSCfamily = models.CharField(max_length=100, choices=(
        ('Customer','Customer'),
        ('Financial','Financial'),
        ('Education and Growth','Education and Growth'),
        ('Internal Processes','Internal Porcesses'),
        ),blank=False, null=True)

    def save(self,*args,**kwargs): # this allow to automatically save the last modified field
        self.updated = timezone.now()
        super(KPI,self).save(*args,**kwargs)
    def __str__(self):
        return self.name

class Objective(models.Model):
    name = models.TextField(null=True,unique=True)
    explanation = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    updated = models.DateField(auto_now_add=True)
    UserType = models.CharField(max_length=100, choices=(
        ('Service User','Service User'),
        ('Data Provider','Data Provider'),
        ('Service Stakeholder','Service Stakeholder'),
        ),blank=False, null=True)
    def save(self,*args,**kwargs): # this allow to automatically save the last modified field
        self.updated = timezone.now()
        super(Objective,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class Criteria(models.Model):
    name = models.TextField(null=True,unique=True)
    explanation = models.TextField(null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    updated = models.DateField(auto_now_add=True)
    Options = models.CharField(max_length=100, choices=(
        ('Cost and Cost Reduction','Cost and Cost Reduction'),
        ('Productivity Increase','Productivity Increase'),
        ('Quality of Data Increase','Quality of Data Increase'),
        ('Safety Increase','Safety Increase'),
        ('Learning and Growth Increase','Learning and Growth Increase'),
        ('User Satisfaction','User Satisfaction'),
        ),blank=False, null=True)
    def save(self,*args,**kwargs): # this allow to automatically save the last modified field
        self.updated = datetime.datetime.today()
        super(Criteria,self).save(*args,**kwargs)

    def __str__(self):
        return self.name

class EVALUATION(models.Model):
    # User information
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    notes = models.TextField()
    ANPAHP_recommendations = models.TextField(blank=True,null=True,default="")
    porcentage = models.TextField(null=True,default="") # this is the % on how ready is the service
    last_modified = models.DateTimeField(auto_now_add=True)
    publication_date = models.DateTimeField(auto_now_add=True)
    action = models.TextField(null=True,default="")
    UserType = models.CharField(max_length=100, choices=(
        ('Service User','Service User'),
        ('Data Provider','Data Provider'),
        ('Service Stakeholder','Service Stakeholder'),
        ),blank=False, null=True)
    #Stages
    status1 = models.BooleanField(default=False)
    status2 = models.BooleanField(default=False)
    status3 = models.BooleanField(default=False)
    status4 = models.BooleanField(default=False)
    status5 = models.BooleanField(default=False)
    status6 = models.BooleanField(default=False)
    status7 = models.BooleanField(default=False)
    status8 = models.BooleanField(default=False)
    ############### these are exclusive for the KPIs.
    KPIs = models.ManyToManyField(KPI, blank=True)
    SelectedKPIs =  models.TextField(null=True,default="[]")
    Scores1 = models.JSONField(null=True,default=dict) # This is for finance the pariwise matrix
    Scores2 = models.JSONField(null=True,default=dict) # this is for internal processes the pairwise matrix
    Scores3 = models.JSONField(null=True,default=dict) # this is for learn and growth the pairwise matrix
    Scores4 = models.JSONField(null=True,default=dict) # this is for clients the pairwise matrix
    inconcistency1 = models.TextField(blank=True,null=True,default="[]")
    inconcistency2 = models.TextField(blank=True,null=True,default="[]")
    inconcistency3 = models.TextField(blank=True,null=True,default="[]")
    inconcistency4 = models.TextField(blank=True,null=True,default="[]")
    vector1 = models.JSONField(null=True,default=dict)
    vector2 = models.JSONField(null=True,default=dict)
    vector3 = models.JSONField(null=True,default=dict)
    vector4 = models.JSONField(null=True,default=dict)
    pairwise_combinations = models.JSONField(null=True,default=dict) # this is to keep the dictionary of paiwise comparison
    KPIS_selected_names = models.TextField(blank=True,null=True,default="[]")
    ################# OBJECTIVES
    Objectives = models.ManyToManyField(Objective, blank=True)
    SelectedObjectives = models.TextField(null=True,default="[]")
    Scores5 = models.JSONField(null=True,default=dict)
    inconcistency5 = models.TextField(blank=True,null=True,default="[]")
    vector5 = models.JSONField(null=True,default=dict)
    pairwise_combinations_objectives = models.JSONField(null=True,default=dict)
    ################# CRITERIA
    BSC_Weights = models.TextField(blank=True,null=True,default="[]")
    Criterias = models.ManyToManyField(Criteria, blank=True)
    SelectedCriterias = models.TextField(null=True,default="[]")
    Scores6 = models.JSONField(null=True,default=dict)
    inconcistency6 = models.TextField(blank=True,null=True,default="[]")
    vector6 = models.JSONField(null=True,default=dict)
    pairwise_combinations_criterias = models.JSONField(null=True,default=dict)
    Criterias_selected_names = models.TextField(blank=True,null=True,default="[]")
    ############### RESULTS
    shapes = models.TextField(blank=True,null=True,default="[]")
    matrix_data = models.JSONField(null=True,default=dict)
    matrix_data_pre = models.TextField(null=True,default="[]")
    results = models.TextField(null=True,default="[]")
    hierarcy = models.TextField(null=True,default="[]")
    supermatrix = models.TextField(null=True,default="[]")
    rows = models.TextField(null=True,default="[]")
    ############## these are for the risk register ################################
    # general comments
    comments = models.TextField(null=True,default="")
    message = models.TextField(null=True,default="")
    ##################################

    User_domain = models.CharField(max_length=100, choices=(
        ('Manufacturing','Manufacturing'),
        ('Aerospace','Aerospace'),
        ('Communications','Communications'),
        ('Chemical and Pharmaceutical','Chemical and pharmaceutical'),
        ('Consumer, Goods and Retail','Consumer, Goods and Retail'),
        ('Energy and Utilities','Energy and Utilities'),
        ('Financial services, Banking and Insurance','Financial services, Banking and Insurance'),
        ('Freight, Logistics and Transportation','Freight, Logistics and Transportation'),
        ('Health and Life Sciences','Health and Life Sciences'),
        ('Hospitality and travel','Hospitality and travel'),
        ('Media, entertainment, and publishing','Media, entertainment, and publishing'),
        ('R&D and Education','R&D and Education'),

        ),blank=False, null=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self): # a get_aboslute_url is a function defined to our class than when is used in a POST method it will reverse to the described url.
        return reverse('taiprm_home', args=(str(self.id)))

    def save(self,*args,**kwargs): # this allow to automatically save the last modified field
        self.porcentage="width: "+str(int(100*(int(self.status1==True)+int(self.status2==True)+int(self.status3==True)+int(self.status4==True)+int(self.status5==True)+int(self.status6==True)+int(self.status7==True)+int(self.status8==True))/4))+"%"
        self.last_modified = datetime.datetime.today()
        super(EVALUATION,self).save(*args,**kwargs)



