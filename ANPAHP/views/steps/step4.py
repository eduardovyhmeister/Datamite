from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from ...utils.helpers import slug_equal
from ...forms import KPIPreferencesForm
from ...models import Evaluation, KPI


@login_required
def step4_view(request, pk):
    """View for step 4: selection of KPIs/metrics preferences."""
    
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    if request.method == 'POST':
        form = KPIPreferencesForm(ANPAHP.kpis, request.POST)
        if form.is_valid():
            # Save the preferences:
            ANPAHP.kpis_preferences = form.retrieve_preferences()
            if ANPAHP.tracker.has_changed('kpis_preferences'):
                ANPAHP.current_step = 4
                ANPAHP.save()
            
            # return render(request, 'ANPAHP/steps/ANPAHPStep4.html', {
            #     'form': form,
            #     'ANPAHP': ANPAHP,
            #     'selected_kpis': ANPAHP.kpis.all().order_by(Lower('name')),
            # })
            return redirect('myANPAHPStep5', pk = ANPAHP.pk)
    else:
        form = KPIPreferencesForm(ANPAHP.kpis, preferences = ANPAHP.kpis_preferences)

    return render(request, 'ANPAHP/steps/ANPAHPStep4.html', {
        'form': form,
        'ANPAHP': ANPAHP,
        'selected_kpis': ANPAHP.kpis.all().order_by(Lower('name')), # Required to be able to iterate in the HTML
    })
