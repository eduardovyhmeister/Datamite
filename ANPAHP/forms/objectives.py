from django.forms import ModelForm, RadioSelect
from django import forms
from django.core.exceptions import ValidationError

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

        
# ----------------------------------------------------------------------------
 
        
class CreateObjectiveForm(ModelForm):
    """Objective creation form."""
    
    class Meta:
        model = Objective
        fields = ('name', 'short_definition', 'explanation')
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs = {'class': 'input',
                                            'placeholder': 'Name for your objective (has to be unique).'}), 
            'short_definition': forms.Textarea(attrs = {'class': 'input',
                                                        'placeholder': 'A short definition of the objective (shown in the objective selection).'}),
            'explanation': forms.Textarea(attrs = {'class': 'input',
                                                   'placeholder':'The long explanation of your objective (used in the knowledge base).'}),
            }
        labels = {
            'name': 'Objective Name',
            'short_definition': 'Short Description',
            'explanation': 'Detailed Explanation',
        }
    
    def clean_name(self):
        """Used to display a user-friendly error message in case the provided
        name isn't unique."""
        name = self.cleaned_data['name']
        if Objective.objects.filter(name = name).exists():
            raise ValidationError("An objective with this name already exists. Please choose a unique name.")
        return name
    
    
# -----------------------------------------------------------------------------


class DeleteObjectiveForm(forms.Form):
    """Form for deleteting an objective."""
    
    objective = forms.ModelChoiceField(
        queryset = Objective.objects.none(),  # set dynamically in the view
        label = "Select an objective to delete",
        widget = forms.Select
    )