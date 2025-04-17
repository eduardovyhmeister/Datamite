"""A module for forms concerning user preferences. Contains forms for
selecting preferences about BSCFamily/Subfamily, KPIs, etc."""

from django.utils.text import slugify
from django import forms

from ..models import BSCFamily


# -----------------------------------------------------------------------------


class BSCPreferencesForm(forms.Form):
    """A form for defining preferences in terms of BSC Subfamilies
    in an ANP-AHP evaluation."""
    
    def __init__(self, *args, preferences = None, **kwargs):
        """Overrides the constructor.
        
        Args:
            preferences (dict): The dictionary of preferences saved in field
                'bsc_preferences' in the 'Evaluation' model.
        """
        super().__init__(*args, **kwargs)
        preferences = preferences or {} # empty dict if None

        for family in BSCFamily.objects.all():
            slug = slugify(family.name)
            initial_value = preferences.get(family.name, 0) # Default value of 0
            
            self.fields[slug] = forms.IntegerField(
                label = family.name,
                min_value = 0,
                max_value = 100,
                initial = initial_value,
                widget = forms.NumberInput(attrs = {
                    'type': 'range',
                    'min': '0',
                    'max': '100',
                    'step': '1',
                    'class': 'slider',
                    'oninput': f'document.getElementById("value_{slug}").value = this.value',
                    'name': slug
                })
            )
            
            
# -----------------------------------------------------------------------------


class KPIPreferencesForm(forms.Form):
    """A form for defining preferences in terms of KPIs/metrics
    in an ANP-AHP evaluation."""
    
    def __init__(self, selected_kpis, *args, preferences = None, **kwargs):
        """Overrides the constructor.
        
        Args:
            selected_kpis (ManyToManyField): The KPIs/metrics selected by the
                user. Can be found in 'Evaluation.kpis'
            preferences (dict): The dictionary of preferences saved in field
                'kpis_preferences' in the 'Evaluation' model.
        """
        super().__init__(*args, **kwargs)
        preferences = preferences or {} # empty dict if None

        for kpi in selected_kpis.order_by('name'):
            slug = slugify(kpi.name)
            initial_value = preferences.get(kpi.name, 1) # Default value of 1
            
            self.fields[slug] = forms.IntegerField(
                label = kpi.name,
                min_value = 1,
                max_value = 100,
                initial = initial_value,
                widget = forms.NumberInput(attrs = {
                    'type': 'range',
                    'min': '1',
                    'max': '100',
                    'step': '1',
                    'class': 'slider',
                    'oninput': f'document.getElementById("value_{slug}").value = this.value',
                    'name': slug
                })
            )