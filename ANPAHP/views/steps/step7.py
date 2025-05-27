from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from ...forms import KPIRelationshipForm
from ...models import Evaluation, KPI


# This a formset that will enable having multiple KPIRelationshipForms
# on the same step page:
KPIRelationshipFormSet = formset_factory(KPIRelationshipForm, extra=1, can_delete=True)
    

@login_required
def step7_view(request, pk):
    """View for step 7: selection of interfamily relationships."""
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    # Generate for each selected KPI, the list of other selected KPIs
    # that are NOT from the same BSC Family.
    kpi_lists = {}
    for kpi1 in ANPAHP.kpis.all():
        kpi_lists[kpi1.name] = []
        for kpi2 in ANPAHP.kpis.all():
            if not kpi1.shares_same_family(kpi2):
                kpi_lists[kpi1.name].append(kpi2.name)
        if not kpi_lists[kpi1.name]: # If empty list
            del kpi_lists[kpi1.name]
    
    if request.method == 'POST':
        # Construct the formset and enable the validity check by adding the
        # acceptable query set to each form.
        formset = KPIRelationshipFormSet(request.POST)
        for form in formset:
            form.fields['main_kpi'].queryset = ANPAHP.kpis.all()
            form.fields['dependencies'].queryset = ANPAHP.kpis.all() # Cannot be more specific, doesn't know the selected KPI yet.

        relationships = {}
        for form in formset:
            if form.is_valid():
                if ('main_kpi' not in form.cleaned_data or 
                    'dependencies' not in form.cleaned_data): 
                    continue # Ignore deleted, empty or half-filled forms.
                
                main_kpi = form.cleaned_data['main_kpi']
                dependencies = form.cleaned_data['dependencies']
                relationships[main_kpi.name] = [dep.name for dep in dependencies]

        ANPAHP.interfamily_relationships = relationships
        ANPAHP.save()  
            
        return render(request, 'ANPAHP/steps/ANPAHPStep7.html', {
            'formset': formset,
            'ANPAHP': ANPAHP,
            'kpi_lists': kpi_lists,
        })
        # return redirect('myANPAHPStep8', pk = ANPAHP.pk)
    else: # GET request
        # Set the formset with the already existing data if it exists:
        initial_data = []
        if ANPAHP.interfamily_relationships:
            for main_kpi, dependencies in ANPAHP.interfamily_relationships.items():
                initial_data.append({
                    'main_kpi': KPI.objects.get(name = main_kpi),
                    'dependencies': list(KPI.objects.filter(name__in = dependencies))
                })
        formset = KPIRelationshipFormSet(initial = initial_data)
        # formset = KPIRelationshipFormSet()
        for form in formset:
            form.fields['main_kpi'].queryset = ANPAHP.kpis.all()
            form.fields['dependencies'].queryset = ANPAHP.kpis.all()

        return render(request, 'ANPAHP/steps/ANPAHPStep7.html', {
            'formset': formset,
            'ANPAHP': ANPAHP,
            'kpi_lists': kpi_lists,
        })