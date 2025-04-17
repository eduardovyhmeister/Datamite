from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...models import Evaluation
from ...forms import CriteriaSelectionForm


@login_required
def step5_view(request, pk):
    """View for step 5: KPIs/metrics selection."""
    
    ANPAHP = Evaluation.objects.get(pk = pk)
    form = CriteriaSelectionForm(request.POST or None,
                                 instance = ANPAHP)
    
    content = {'ANPAHP': ANPAHP,
               'form': form,
               }
    
    if request.method == "POST":
        if request.POST.get("action") == "confirm": # Only present when clicking confirm
            if form.is_valid():
                form.save()
                ANPAHP.current_step = 5
                ANPAHP.save()
                # return render(request, 'ANPAHP/steps/ANPAHPStep5.html', content)
                return redirect('myANPAHPStep6', pk = ANPAHP.pk)
        
    return render(request, 'ANPAHP/steps/ANPAHPStep5.html', content)