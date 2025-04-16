from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...models import Evaluation, KPI
from ...forms import KPISelectionForm


@login_required
def step3_view(request, pk):
    """View for step 3: KPIs/metrics selection."""
    
    ANPAHP = Evaluation.objects.get(pk = pk)
    form = KPISelectionForm(request.POST or None,
                            instance = ANPAHP)
    
    content = {'ANPAHP': ANPAHP,
               'form': KPISelectionForm(request.POST or None, 
                                        instance = ANPAHP),
               }
    
    if request.method == "POST":
        print("POST DATA:", request.POST)
        if request.POST.get("action") == "confirm": # Only present when clicking confirm
            if form.is_valid():
                form.save()
                ANPAHP.step_status3 = True
                ANPAHP.save()
                return render(request, 'ANPAHP/steps/ANPAHPStep3.html', content)
                #return redirect('myANPAHPStep4', pk = ANPAHP.pk)
        
    return render(request, 'ANPAHP/steps/ANPAHPStep3.html', content)