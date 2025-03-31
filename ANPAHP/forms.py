from random import choices
from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxSelectMultiple, widgets, ModelForm, formset_factory

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2',)
        widgets = {
            'username' : forms.TextInput(attrs={'class':'input'}),
            'email' : forms.EmailInput(attrs={'class':'input'}),
            'password1' : forms.PasswordInput(attrs={'class':'input'}),
            'password2' : forms.PasswordInput(attrs={'class':'input'}),
        }


class ANPAHPForm(ModelForm):
    class Meta:
        model = EVALUATION # with wat model you want to work
        fields = ('title','UserType')
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={'class':'input','placeholder':'title'}), # top set an input format with bootstrap form
            'UserType': forms.Select(choices=[('Service User','Service User'),('Data Provider','Data Provider'),('Service Stakeholder','Service Stakeholder')]),
        }

class NotesForm(ModelForm):
    class Meta:
        model = EVALUATION
        fields = ('notes',)


class   Step1Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        KPIs = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'KPIs' : CheckboxSelectMultiple(),
        }


class   Step2Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step3Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step4Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step5Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step6Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        Objectives = forms.ModelMultipleChoiceField(queryset=Objective.objects.all())
        fields = ['Objectives']
        widgets = {
            'Objectives' : CheckboxSelectMultiple(),
        }

class   Step8Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        Criterias = forms.ModelMultipleChoiceField(queryset=Criteria.objects.all().order_by('name'))
        fields = ['Criterias']
        widgets = {'Criterias' : CheckboxSelectMultiple(),
        }

#class Step8Form(forms.ModelForm):
#    Criterias = forms.ModelMultipleChoiceField(
#        queryset=Criteria.objects.all().order_by('name'),  # Order alphabetically by name
#        widget=CheckboxSelectMultiple()
#    )
#    class Meta:
#        model = EVALUATION
#        fields = ['Criterias']


class   Step9Form(forms.ModelForm):
      class Meta:
        model = EVALUATION
        KPIs = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        Criterias = forms.ModelMultipleChoiceField(queryset=Criteria.objects.all())
        fields = ['Criterias','KPIs']
        widgets = {
            'Criterias' : CheckboxSelectMultiple(),
            'KPIs' : CheckboxSelectMultiple(),
        }



class NewKPIForm(ModelForm):
    class Meta:
        model = KPI # with wat model you want to work
        fields = ('name','explanation','BSCfamily',)
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs={'class':'input','placeholder':'Name for your KPI'}), # top set an input format with bootstrap form
            'explanation': forms.Textarea(attrs={'class':'input','placeholder':'Provide some exemplification for other to understand'}),
            #'BSCfamily': forms.Textarea(attrs={'class':'input','placeholder':'BSCfamily from your KPI'}),
            'BSCfamily': forms.Select(choices=[('Clients','Clients'),('Finance','Finance'),('Internal Process','Internal Process'),('Learn and Growth','Learn and Growth')]),
        }

class NewObjectivesForm(ModelForm):
    class Meta:
        model = Objective # with wat model you want to work
        fields = ('name','explanation','UserType')
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs={'class':'input','placeholder':'Name for your KPI'}), # top set an input format with bootstrap form
            'explanation': forms.Textarea(attrs={'class':'input','placeholder':'Provide some exemplification for other to understand'}),
            'UserType': forms.Select(choices=[('Service User','Service User'),('Data Provider','Data Provider'),('Service Stakeholder','Service Stakeholder')]),
        }

class NewCriteriaForm(ModelForm):
    class Meta:
        model = Criteria # with wat model you want to work
        fields = ('name','explanation')
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs={'class':'input','placeholder':'Name for your KPI'}), # top set an input format with bootstrap form
            'explanation': forms.Textarea(attrs={'class':'input','placeholder':'Provide some exemplification for other to understand'}),
        }


class Results1Form(ModelForm):
    class Meta:
        model = EVALUATION
        fields = ['results','ANPAHP_recommendations']
        widgets = {
            'results': forms.Textarea(attrs={'class':'input','placeholder':'Recommendations'}),
            'ANPAHP_recommendations': forms.Textarea(attrs={'class':'input','placeholder':'Recommendations for the Tool'})
        }


