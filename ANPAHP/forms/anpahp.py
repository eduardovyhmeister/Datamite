from django.forms import ModelForm, TextInput, Select

from ..models import Evaluation
from ..models.enumerations import UserType


class ANPAHPForm(ModelForm):
    """Form for creating a new ANP-AHP Evaluation"""

    class Meta:
        model = Evaluation
        fields = ('name', 'user_type')
        exclude = ('author',)
        widgets = {
            'name': TextInput(attrs = {'class':'input', 'placeholder':'Name of your evaluation'}), # top set an input format with bootstrap form
            'user_type': Select(choices = UserType),
        }