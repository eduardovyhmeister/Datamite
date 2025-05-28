"""A module for forms concerning user preferences. Contains forms for
selecting preferences about BSCFamily/Subfamily, KPIs, etc.

`PreferencesSelectionForm` offers a generic preference selection which will,
given a selection of objects, provide a slider and a text box (both linked to it via
JS) for a user to select a preference score (by default, from 0 to 100)."""

from django.utils.text import slugify
from django import forms
from django.db.models.functions import Lower

from ..models import BSCFamily
from ..utils.helpers import slug_equal


# -----------------------------------------------------------------------------


class PreferencesSelectionForm(forms.Form):
    """A generic form for selecting preferences (with sliders, etc.)."""

    def __init__(self, selected_objs, *args, 
                 min_value = 0, max_value = 100, step = 1,
                 preferences = None, preference_field = 'name', **kwargs):
        """Overrides the constructor adding a few parameters.
        
        Args:
            selected_objs (queryset): The objects to display preferences for 
                (e.g. 'BSCFamily.objects.all()'), usually selected in the previous step.
            min_value (int/float): The minimum value for the preference (defaults to 0).
            max_value (int/float): The maximum value for the preference (defaults to 100).
            step (int/float): The step used between two values on the slider (defaults to 1).
            selected_objs (queryset): A selection of model instances for which preferences
                need to be set (basically the list of object to get sliders for).
            preferences (dict[obj: value]): The dictionary of already existing
                preferences to set the initial values. It needs to be a dictionary
                of objects retrievable as unique/primary keys as a key (defaults to
                str for field 'name' of the model) and a valid value as decided by 
                'min_value' and 'max_value'.
            preference_field (str): The name of the field to retrieve the objects for
                to set the initial values of the preferences. That field should have
                values that can serve as keys of a dictionary (defaults to 'name').
        """
        super().__init__(*args, **kwargs)
        self.selected_objs = selected_objs
        self.preference_field = preference_field
        preferences = preferences or {} # empty dict if None

        for obj in selected_objs:
            slug = slugify(str(getattr(obj, preference_field))) # Required to be JS-friendly
            initial_value = preferences.get(getattr(obj, preference_field), min_value) # Default to min_value
            
            self.fields[slug] = _SliderWithNumberMultiValueField(
                name = slug,
                min_value = min_value,
                max_value = max_value,
                initial_value = initial_value,
            )

            
    def retrieve_preferences(self):
        """Provides the dictionary of preferences with un-slugified fields. Use this
        to retrieve the data provided by the user properly.
        
        Returns:
            dict[obj: value] - The dictionary of preferences. Keys are objects contained
            in 'preference_field' as specified in the constructor. Values are the preferences
            values set by the user.
        """
        preferences = {}
        # Extract preferences properly by matching form field names:
        # Necessary because JS doesn't like non-slug names.
        for obj in self.selected_objs:
            for slug_name, value in self.cleaned_data.items():
                if slug_equal(str(getattr(obj, self.preference_field)), slug_name):
                    preferences[getattr(obj, self.preference_field)] = value
        return preferences

# -----------------------------------------------------------------------------


class BSCPreferencesForm(PreferencesSelectionForm):
    """A form for defining preferences in terms of BSC families in an ANP-AHP evaluation.
    It is just a 'PreferencesSelectionForm' create with specific parameters."""
    
    def __init__(self, *args, preferences = None, **kwargs):
        """Overrides the constructor to create the form with specific values.
        
        Args:
            preferences (dict[str: int]): The preferences previously selected by the user.
        """
        super().__init__(
            BSCFamily.objects.all().order_by(Lower('name')),
            *args, 
            min_value = 0,
            max_value = 100,
            step = 1,
            preferences = preferences,
            preference_field = 'name',
            **kwargs
            )
            
            
# -----------------------------------------------------------------------------


class KPIPreferencesForm(PreferencesSelectionForm):
    """A form for defining preferences in terms of KPIs/metrics in an ANP-AHP evaluation.
    It is just a 'PreferencesSelectionForm' create with specific parameters."""
    
    def __init__(self, selected_kpis, *args, preferences = None, **kwargs):
        """Overrides the constructor to create the form with specific values.
        
        Args:
            selected_kpis (queryset): The KPIs/metrics selected by the user. This is
                used as 'selected_objs' in the constructor of 'PreferencesSelectionForm'.
            preferences (dict[str: int]): The preferences previously selected by the user.
        """
        super().__init__(
            selected_kpis.order_by(Lower('name')),
            *args, 
            min_value = 1,
            max_value = 100,
            step = 1,
            preferences = preferences,
            preference_field = 'name',
            **kwargs
            )

            
# -----------------------------------------------------------------------------


class CriteriaPreferencesForm(PreferencesSelectionForm):
    """A form for defining preferences in terms of criteria in an ANP-AHP evaluation.
    It is just a 'PreferencesSelectionForm' create with specific parameters."""
    
    def __init__(self, selected_criteria, *args, preferences = None, **kwargs):
        """Overrides the constructor to create the form with specific values.
        
        Args:
            selected_criteria (queryset): The criteria selected by the user. This is
                used as 'selected_objs' in the constructor of 'PreferencesSelectionForm'.
            preferences (dict[str: int]): The preferences previously selected by the user.
        """
        super().__init__(
            selected_criteria.order_by(Lower('name')),
            *args, 
            min_value = 1,
            max_value = 100,
            step = 1,
            preferences = preferences,
            preference_field = 'name',
            **kwargs
            )


# -----------------------------------------------------------------------------
# Private classes used for creating the multi-widget element for preferences
# (slider + text number input) and the multi-value field that uses such a widget.


class _SliderWithNumberWidget(forms.MultiWidget):
    """Private class for combining the slider and the number input as text
    into a single widget."""
    
    def __init__(self, name, min_value=0, max_value=100, step=1):
        """Constructor of the multi-widget.
        
        Args:
            name (str): The name used for IDs (will be slugified).
            min_value (int/float): The minimum value for the slider/number
                input (defaults to 0).
            max_value (int/float): The maximum value for the slider/number
                input (defaults to 100).
            step (int/float): The step for increments of the value of the
                widget (defaults to 1).
        """
        widgets = [
            forms.NumberInput(attrs={
                'type': 'range',
                'class': 'slider',
                'min': str(min_value),
                'max': str(max_value),
                'step': str(step),
                'id': f'slider_{slugify(name)}',
                'oninput': f'this.nextElementSibling.value = this.value'
            }),
            forms.NumberInput(attrs={
                'type': 'number',
                'class': 'numeric_value',
                'min': str(min_value),
                'max': str(max_value),
                'step': str(step),
                'id': f'num_{slugify(name)}',
                'oninput': 'this.previousElementSibling.value = this.value'
            }),
        ]
        super().__init__(widgets)

    def decompress(self, value):
        """Returns the value corresponding to the widget as a whole.
        DOT NOT DELETE THIS METHOD, you'll get NotImplementedError."""
        return value
    
    
class _SliderWithNumberMultiValueField(forms.MultiValueField):
    """Private class for a multi-value field using the multi-widget defined above.
    Will effectively contain a single value because both widgets synchronise their
    values."""
    
    def __init__(self, name, min_value=0, max_value=100, step=1, initial_value=None, **kwargs):
        """Constructor of the multi-value field.
        
        Args:
            name (str): Name of the field, used as an ID for widgets, will be slugified.
            min_value (int/float): The minimum value for the slider/number
                input (defaults to 0).
            max_value (int/float): The maximum value for the slider/number
                input (defaults to 100).
            step (int/float): The step for increments of the value of the
                widget (defaults to 1).
            initial_value (int/float): The initial value the field should have
                (specify this to display your loaded data for instance). If set
                to `None` will default to `min_value` (defaults to `None`).
        """
        initial_value = initial_value if initial_value is not None else min_value
        super().__init__(
            fields = [
                forms.IntegerField(min_value=min_value, max_value=max_value),
                forms.IntegerField(min_value=min_value, max_value=max_value),
            ],
            initial = [initial_value, initial_value],
            widget = _SliderWithNumberWidget(slugify(name), min_value=min_value, max_value=max_value, step=step),
            **kwargs
        )
    
    def compress(self, data_list):
        """Returns the value corresponding to the field.
        DOT NOT DELETE THIS METHOD, you'll get NotImplementedError."""
        return data_list[0]
