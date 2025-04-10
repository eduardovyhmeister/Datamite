from random import choices
from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import CheckboxSelectMultiple, widgets, ModelForm, formset_factory

from .models import (BSCFamily,
                     BSCSubfamily,
                     Criterion, 
                     Evaluation, 
                     KPI, 
                     Objective)


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
        model = Evaluation # with wat model you want to work
        fields = ('title','user_type')
        exclude = ('author',)
        widgets = {
            'title': forms.TextInput(attrs={'class':'input','placeholder':'title'}), # top set an input format with bootstrap form
            'user_type': forms.Select(choices=[('Service User','Service User'),('Data Provider','Data Provider'),('Service Stakeholder','Service Stakeholder')]),
        }

class NotesForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ('notes',)


class   Step1Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        KPIs = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'KPIs' : CheckboxSelectMultiple(),
        }


class   Step2Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step3Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step4Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step5Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        FailureModes = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        fields = ['KPIs']
        widgets = {
            'FailureModes' : CheckboxSelectMultiple(),
        }

class   Step6Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        objectives = forms.ModelMultipleChoiceField(queryset=Objective.objects.all())
        fields = ['objectives']
        widgets = {
            'objectives' : CheckboxSelectMultiple(),
        }

class   Step8Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        criteria = forms.ModelMultipleChoiceField(queryset=Criterion.objects.all().order_by('name'))
        fields = ['criteria']
        widgets = {'criteria' : CheckboxSelectMultiple(),
        }

#class Step8Form(forms.ModelForm):
#    Criterions = forms.ModelMultipleChoiceField(
#        queryset=Criterion.objects.all().order_by('name'),  # Order alphabetically by name
#        widget=CheckboxSelectMultiple()
#    )
#    class Meta:
#        model = Evaluation
#        fields = ['Criterions']


class   Step9Form(forms.ModelForm):
      class Meta:
        model = Evaluation
        KPIs = forms.ModelMultipleChoiceField(queryset=KPI.objects.all())
        Criterions = forms.ModelMultipleChoiceField(queryset=Criterion.objects.all())
        fields = ['criteria','KPIs']
        widgets = {
            'criteria' : CheckboxSelectMultiple(),
            'KPIs' : CheckboxSelectMultiple(),
        }



class NewKPIForm(ModelForm):
    class Meta:
        model = KPI # with wat model you want to work
        fields = ('name','explanation','bsc_subfamilies',)
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs={'class':'input','placeholder':'Name for your KPI'}), # top set an input format with bootstrap form
            'explanation': forms.Textarea(attrs={'class':'input','placeholder':'Provide some exemplification for other to understand'}),
            #'bsc_family': forms.Textarea(attrs={'class':'input','placeholder':'bsc_family from your KPI'}),
            #'bsc_subfamily': forms.Select(choices=[('Clients','Clients'),('Finance','Finance'),('Internal Process','Internal Process'),('Learn and Growth','Learn and Growth')]),
            'bsc_subfamilies': forms.ModelMultipleChoiceField(queryset = BSCSubfamily.objects.all())
        }

class NewObjectivesForm(ModelForm):
    class Meta:
        model = Objective # with wat model you want to work
        fields = ('name','explanation')
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs={'class':'input','placeholder':'Name for your KPI'}), # top set an input format with bootstrap form
            'explanation': forms.Textarea(attrs={'class':'input','placeholder':'Provide some exemplification for other to understand'}),
            }

class NewCriterionForm(ModelForm):
    class Meta:
        model = Criterion # with wat model you want to work
        fields = ('name','explanation')
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs={'class':'input','placeholder':'Name for your KPI'}), # top set an input format with bootstrap form
            'explanation': forms.Textarea(attrs={'class':'input','placeholder':'Provide some exemplification for other to understand'}),
        }


class Results1Form(ModelForm):
    class Meta:
        model = Evaluation
        fields = ['results','ANPAHP_recommendations']
        widgets = {
            'results': forms.Textarea(attrs={'class':'input','placeholder':'Recommendations'}),
            'ANPAHP_recommendations': forms.Textarea(attrs={'class':'input','placeholder':'Recommendations for the Tool'})
        }


