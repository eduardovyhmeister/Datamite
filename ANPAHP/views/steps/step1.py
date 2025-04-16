from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...models import Evaluation
from ...forms import ObjectiveSelectionForm

@login_required
def step1_view(request, pk):
    """View for step 1: selection of an objective."""
    
    ANPAHP = Evaluation.objects.get(pk = pk)
    form = ObjectiveSelectionForm(request.POST or None, instance = ANPAHP)
    
    content = {'ANPAHP': ANPAHP,
               'form': ObjectiveSelectionForm(request.POST or None, 
                                              instance = ANPAHP),
               }
    
    if request.method == "POST":
        if request.POST.get("action") == "confirm": # Only present when clicking confirm
            if form.is_valid():
                form.save()
                # Only need to advance to the next step if not more advanced into the process
                # since this step doesn't affect the following steps really:
                if ANPAHP.current_step == 0:
                    ANPAHP.current_step += 1
                    ANPAHP.save()
                return redirect('myANPAHPStep2', pk = ANPAHP.pk)
        
    return render(request, 'ANPAHP/steps/ANPAHPStep1.html', content)

