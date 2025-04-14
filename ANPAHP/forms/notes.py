from django.forms import ModelForm

from ..models import Evaluation


class NotesForm(ModelForm):
    """Form for adding notes to an ANP-AHP Evaluation."""
    class Meta:
        model = Evaluation
        fields = ('notes',)
        
    def __init__(self, *args, **kwargs):
        # Enables Bootstrap formatting for the form:
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'