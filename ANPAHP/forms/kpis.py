from django.forms import ModelForm, CheckboxSelectMultiple
from django import forms 
from django.core.exceptions import ValidationError
from django.db.models.functions import Lower

from ..models import Evaluation, KPI, BSCFamily, BSCSubfamily


class KPISelectionForm(ModelForm):
    """KPI selection form for the ANP-AHP Evaluation."""
    
    # The name here has to match the name of the field to update in Evaluation:
    kpis = forms.ModelMultipleChoiceField(
        queryset = KPI.objects.all().order_by(Lower('name')),
        widget = CheckboxSelectMultiple
    )
    
    class Meta:
        model = Evaluation
        fields = ['kpis']
        
    def __init__(self, *args, **kwargs):
        """Overrides constructor to be able to filter out KPIs that are not relevant
        based on BSC preferences defined in step 2."""
        super().__init__(*args, **kwargs)
        # Filter out the KPIs whose BSC Family has a 0 coefficient set in preferences:
        non_zero_bsc_families = [family_name 
                                 for family_name, value in kwargs["instance"].bsc_preferences.items()
                                 if value > 0]
        non_zero_bsc_families = BSCFamily.objects.filter(name__in = non_zero_bsc_families)
        subfamily_list = BSCSubfamily.objects.filter(bsc_family__in = non_zero_bsc_families)
        filtered_KPIs = KPI.objects.filter(bsc_subfamilies__in = subfamily_list).distinct()
        
        # Order the remaining KPIs alphabetically:
        self.fields['kpis'].queryset = filtered_KPIs.order_by(Lower('name'))
        
        
# ----------------------------------------------------------------------------


class BSCSubfamilyMultipleChoiceField(forms.ModelMultipleChoiceField):
    """Used to override the labels for the selection of subfamilies in the
    CreateKPIForm."""
    
    def label_from_instance(self, obj):
        """Overrides this to format the label string as you please."""
        return f"{obj.bsc_family.name} — {obj.name}"

        
class CreateKPIForm(forms.ModelForm):
    """Form used for the creation of a new KPI into the DB."""
    
    alternative_names = forms.CharField(
        required = False,
        widget = forms.Textarea(attrs = {
            'placeholder': 'Enter a list of alternative names, separated by commas. Used for the knowledge base.',
            'rows': 2,
        }),
        help_text = 'Optional. Example: "ROI, Return on Investment"',
        label = 'Alternative Names'
    )

    bsc_subfamilies = BSCSubfamilyMultipleChoiceField(
        queryset = BSCSubfamily.objects.all().order_by("bsc_family__name", "name"), # Order first by BSC family, then by name
        widget = forms.SelectMultiple(attrs = {'size': '6'}),
        help_text = 'Select at least one BSC subfamily. Ctrl + click to select multiple subfamilies.',
        label = 'BSC Subfamilies'
    )

    class Meta:
        model = KPI
        fields = ['name', 'alternative_names', 'bsc_subfamilies', 'short_definition', 'explanation']
        widgets = {
            'name': forms.Textarea(attrs = {'rows': 1,
                                            'placeholder': 'Name for your KPI (has to be unique).'}),
            'short_definition': forms.Textarea(attrs = {'rows': 2,
                                                        'placeholder': 'A short definition of the KPI/metric (shown in the KPI/metric selection).'}),
            'explanation': forms.Textarea(attrs={'rows': 6,
                                                 'placeholder': 'The long explanation of your KPI/metric (used in the knowledge base).'}),
        }
        labels = {
            'name': 'KPI/metric Name',
            'short_definition': 'Short Description',
            'explanation': 'Detailed Explanation',
        }
        

    def clean_alternative_names(self):
        """Cleans the provided list of names to get rid of extra spaces, etc."""
        raw = self.cleaned_data['alternative_names']
        if not raw.strip():
            return []
        return [name.strip() for name in raw.split(',') if name.strip()]


    def clean_bsc_subfamilies(self):
        """Checks that at least one BSC subfamily has been selected."""
        subs = self.cleaned_data.get('bsc_subfamilies')
        if not subs or len(subs) < 1:
            raise ValidationError('Please select at least one BSC subfamily.')
        return subs
    
    
    def clean_name(self):
        """Used to display a user-friendly error message in case the provided
        name isn't unique."""
        name = self.cleaned_data['name']
        if KPI.objects.filter(name = name).exists():
            raise ValidationError("A KPI with this name already exists. Please choose a unique name.")
        return name
    
    
# -----------------------------------------------------------------------------


class DeleteKPIForm(forms.Form):
    """Form for deleteting an KPI."""
    
    kpi = forms.ModelChoiceField(
        queryset = KPI.objects.none(),  # set dynamically in the view
        label = "Select a KPI/metric to delete",
        widget = forms.Select
    )