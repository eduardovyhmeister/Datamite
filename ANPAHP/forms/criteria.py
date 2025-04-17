from django.core.exceptions import ValidationError
from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms
from django.db.models.functions import Lower

from ..models import Evaluation, Criterion


class CriteriaSelectionForm(ModelForm):
    """Criteria selection form for the ANP-AHP Evaluation."""
    
    # The name here has to match the name of the field to update in Evaluation:
    criteria = forms.ModelMultipleChoiceField(
        queryset = Criterion.objects.all().order_by(Lower('name')),
        widget = CheckboxSelectMultiple  # or use forms.Select for dropdown
    )
    
    class Meta:
        model = Evaluation
        fields = ['criteria']
        

# ----------------------------------------------------------------------------
 
        
class CreateCriterionForm(ModelForm):
    """Criterion creation form."""
    
    class Meta:
        model = Criterion
        fields = ('name', 'explanation')
        exclude = ('author',)
        widgets = {
            'name': forms.Textarea(attrs = {'class': 'input',
                                            'placeholder': 'Name for your criterion (has to be unique).',
                                            'rows': 1 # Controls the size of the widget to show.
                                            }), 
            'explanation': forms.Textarea(attrs = {'class': 'input',
                                                   'placeholder':'The explanation of your criterion (shown in the criteria selection and used in the knowledge base).'}),
            }
        labels = {
            'name': 'Criterion Name',
            'explanation': 'Explanation',
        }
    
    def clean_name(self):
        """Used to display a user-friendly error message in case the provided
        name isn't unique."""
        name = self.cleaned_data['name']
        if Criterion.objects.filter(name = name).exists():
            raise ValidationError("A criterion with this name already exists. Please choose a unique name.")
        return name
    
    
# -----------------------------------------------------------------------------


class DeleteCriterionForm(forms.Form):
    """Form for deleteting an Criterion."""
    
    criterion = forms.ModelChoiceField(
        queryset = Criterion.objects.none(),  # set dynamically in the view
        label = "Select an criterion to delete",
        widget = forms.Select
    )