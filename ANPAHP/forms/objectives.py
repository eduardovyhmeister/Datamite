from django.forms import ModelForm, RadioSelect
from django import forms 

from ..models import Evaluation, Objective

class ObjectiveSelectionForm(ModelForm):
    """Objective selection form for the ANP-AHP Evaluation."""
    
    # The name here has to match the name of the field to update in Evaluation:
    objective = forms.ModelChoiceField(
        queryset = Objective.objects.all(),
        widget = RadioSelect  # or use forms.Select for dropdown
    )
    
    class Meta:
        model = Evaluation
        fields = ['objective']