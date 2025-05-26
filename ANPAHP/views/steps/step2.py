from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...utils.helpers import slug_equal
from ...forms import BSCPreferencesForm
from ...models import Evaluation, BSCFamily


@login_required
def step2_view(request, pk):
    """View for step 2: selection of BSC families preferences."""
    
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    if request.method == 'POST':
        form = BSCPreferencesForm(request.POST)
        if form.is_valid():
            ANPAHP.bsc_preferences = form.retrieve_preferences()
            if ANPAHP.tracker.has_changed('bsc_preferences'):
                ANPAHP.current_step = 2
            ANPAHP.save()
            
            return redirect('myANPAHPStep3', pk = ANPAHP.pk)
    else:
        form = BSCPreferencesForm(preferences = ANPAHP.bsc_preferences)

    return render(request, 'ANPAHP/steps/ANPAHPStep2.html', {
        'form': form,
        'ANPAHP': ANPAHP,
        'families': BSCFamily.objects.all(),
    })
