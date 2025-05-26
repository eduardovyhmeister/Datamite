"""Forms to manage relationships between KPIs/metrics of different families."""

from django import forms

from ..models import KPI

class KPIRelationshipForm(forms.Form):
    """Form for creating relationships between KPIs from different BSC Families.
    This form will be repeated in a formset, with an 'add' button that users can
    click to add a new one, hence enabling the creation of multiple relationships.
    """
    
    main_kpi = forms.ModelChoiceField(
        queryset = KPI.objects.none(),  # set dynamically in the view
        label = "Select a KPI/metric:",
        widget = forms.Select(attrs = {'class': 'form-control'})
    )
    
    dependencies = forms.ModelMultipleChoiceField(
        queryset = KPI.objects.none(), # Will be set in the HTML/JS directly, once the main KPI is selected.
        label = "KPIs/metrics that may influence the selected KPI:",
        widget = forms.SelectMultiple(attrs = {'size': '6', 'class': 'form-control'}),
        help_text = 'Select at least one KPI/metric. Ctrl + click to select multiple items.',
    )
    
    
# TODO: add the formset for the KPIRelationshipForm

