from django.forms import ModelForm, TextInput, Select

from ..models import Evaluation
from ..models.enumerations import UserType


class ANPAHPForm(ModelForm):
    class Meta:
        model = Evaluation
        fields = ('title', 'user_type')
        exclude = ('author',)
        widgets = {
            'title': TextInput(attrs = {'class':'input', 'placeholder':'title'}), # top set an input format with bootstrap form
            'user_type': Select(choices = UserType),
        }