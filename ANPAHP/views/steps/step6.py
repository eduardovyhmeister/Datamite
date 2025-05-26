from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from ...utils.helpers import slug_equal
from ...forms import CriteriaPreferencesForm
from ...models import Evaluation, Criterion


@login_required
def step6_view(request, pk):
    """View for step 6: selection of criteria preferences."""
    
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    if request.method == 'POST':
        form = CriteriaPreferencesForm(ANPAHP.criteria, request.POST)
        if form.is_valid():
            # Save the preferences:
            ANPAHP.criteria_preferences = form.retrieve_preferences()
            if ANPAHP.tracker.has_changed('criteria_preferences'):
                ANPAHP.current_step = 6
            ANPAHP.save()
            
            # return render(request, 'ANPAHP/steps/ANPAHPStep6.html', {
            #     'form': form,
            #     'ANPAHP': ANPAHP,
            #     'selected_criteria': ANPAHP.criteria.all().order_by(Lower('name')),
            # })
            return redirect('myANPAHPStep7', pk = ANPAHP.pk)
    else:
        form = CriteriaPreferencesForm(ANPAHP.criteria, preferences = ANPAHP.criteria_preferences)

    return render(request, 'ANPAHP/steps/ANPAHPStep6.html', {
        'form': form,
        'ANPAHP': ANPAHP,
        'selected_criteria': ANPAHP.criteria.all().order_by(Lower('name')), # Required to be able to iterate in the HTML
    })