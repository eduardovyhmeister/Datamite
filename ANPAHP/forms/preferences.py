"""A module for forms concerning user preferences. Contains forms for
selecting preferences about BSCFamily/Subfamily, KPIs, etc."""

from django.utils.text import slugify
from django import forms

from ..models import BSCFamily


class BSCPreferencesForm(forms.Form):
    """A form for defining preferences in terms of BSC Subfamilies
    in an ANP-AHP evaluation."""
    
    def __init__(self, *args, **kwargs):
        """Overrides the constructor."""
        super().__init__(*args, **kwargs)

        for subfamily in BSCFamily.objects.all():
            slug = slugify(subfamily.name)
            self.fields[slug] = forms.IntegerField(
                label = subfamily.name,
                min_value = 0,
                max_value = 100,
                initial = 0,
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