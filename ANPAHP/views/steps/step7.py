from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from ...utils.helpers import slug_equal
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
            if kpi1 == kpi2: continue
            if not kpi1.shares_same_family(kpi2):
                kpi_lists[kpi1.name].append(kpi2.name)
        print(kpi1.name, " = ", kpi_lists[kpi1.name])
    
    if request.method == 'POST':
        formset = KPIRelationshipFormSet(request.POST)
        for form in formset:
            form.fields['main_kpi'].queryset = ANPAHP.kpis.all()
        if formset.is_valid():
            # TODO: retrieve the selected KPIs from the form.
            
            return render(request, 'ANPAHP/steps/ANPAHPStep7.html', {
                'formset': formset,
                'ANPAHP': ANPAHP,
                'kpi_lists': kpi_lists,
            })
            # return redirect('myANPAHPStep8', pk = ANPAHP.pk)
    else:
        formset = KPIRelationshipFormSet()
        for form in formset:
            form.fields['main_kpi'].queryset = ANPAHP.kpis.all()

    return render(request, 'ANPAHP/steps/ANPAHPStep7.html', {
        'formset': formset,
        'ANPAHP': ANPAHP,
        'kpi_lists': kpi_lists,
    })