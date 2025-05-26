from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.functions import Lower

from ...utils.helpers import slug_equal
from ...forms import CriteriaPreferencesForm
from ...models import Evaluation, Criterion

@login_required
def step7_view(request, pk):
    """View for step 7: selection of interfamily relationships."""
    
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    if request.method == 'POST':
        # TODO
        form = None
    
        # form = CriteriaPreferencesForm(ANPAHP.criteria, request.POST)
        # if form.is_valid():
        #     # Save the preferences:
        #     ANPAHP.criteria_preferences = form.retrieve_preferences()
        #     if ANPAHP.tracker.has_changed('criteria_preferences'):
        #         ANPAHP.current_step = 6
        #     ANPAHP.save()
            
            # return render(request, 'ANPAHP/steps/ANPAHPStep7.html', {
            #     'form': form,
            #     'ANPAHP': ANPAHP,
            # })
            # return redirect('myANPAHPStep8', pk = ANPAHP.pk)
    else:
        # TODO
        form = None

    return render(request, 'ANPAHP/steps/ANPAHPStep7.html', {
        'form': form,
        'ANPAHP': ANPAHP,
    })