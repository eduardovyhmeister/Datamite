from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from ...forms import KPIPreferencesForm
from ...models import Evaluation, KPI


@login_required
def step8_view(request, pk):
    """View for step 8: selection of interfamily relationships preferences."""
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    # Retrieve the names of the KPIs selected in the previous step:
    main_kpis = KPI.objects.filter(name__in = list(ANPAHP.interfamily_relationships))

    # Build the form set:
    KPIRelationshipPreferenceFormSet = formset_factory(KPIPreferencesForm, extra = 0)
    formset = KPIRelationshipPreferenceFormSet()

    if request.method == 'POST':
        # Create the formset by manually generating the KPIPreferencesForms.
        # It is done manually here to ease the process of passing arguments to the
        # forms' constructor (FormSet doesn't really offer a way to do it right now).
        # I loop over main_kpis to make sure I create the forms in the same order
        # (the order matter in the HTML template later on).
        for kpi in main_kpis:
            formset.forms.append(KPIPreferencesForm(
                KPI.objects.filter(name__in = ANPAHP.interfamily_relationships[kpi.name]), # selected_kpis (required positional argument)
                request.POST,
                preferences = None if ANPAHP.interfamily_preferences is None else ANPAHP.interfamily_preferences[kpi.name],
            ))
        
        # Retrieve all the preferences (in this case they indicate influence importance):
        # KPIs that have only 1 KPI influencing them still appear in the forms, even if not
        # displayed on the webpage. They will have the default "preference" value of 1.
        interfamily_preferences = {}
        for i, form in enumerate(formset):
            if form.is_valid():
                interfamily_preferences[main_kpis[i].name] = form.retrieve_preferences()
        
        ANPAHP.interfamily_preferences = interfamily_preferences
        if ANPAHP.tracker.has_changed('interfamily_preferences'):
            ANPAHP.current_step = 8
            ANPAHP.save()
        
        return render(request, 'ANPAHP/steps/ANPAHPStep8.html', {
            'formset': formset,
            'ANPAHP': ANPAHP,
            'main_kpis': main_kpis,
        })
        # return redirect('myANPAHPResult', pk = ANPAHP.pk)
    else: # GET request
        for kpi in main_kpis:
            formset.forms.append(KPIPreferencesForm(
                selected_kpis = KPI.objects.filter(name__in = ANPAHP.interfamily_relationships[kpi.name]),
                preferences = None if ANPAHP.interfamily_preferences is None else ANPAHP.interfamily_preferences[kpi.name],
            ))
        return render(request, 'ANPAHP/steps/ANPAHPStep8.html', {
            'formset': formset,
            'ANPAHP': ANPAHP,
            'main_kpis': main_kpis,
        })
    