from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...models import Evaluation
from ...forms import ObjectiveSelectionForm

@login_required
def step1_view(request, pk):
    ANPAHP = Evaluation.objects.get(pk = pk)
    form = ObjectiveSelectionForm(request.POST or None, instance = ANPAHP)
    
    content = {'ANPAHP': ANPAHP,
               'form': ObjectiveSelectionForm(request.POST or None, 
                                              instance = ANPAHP),
               }
    
    if request.method == "POST":
        print("POST DATA:", request.POST)
        if request.POST.get("action") == "confirm": # Only present when clicking confirm
            if form.is_valid():
                form.save()
                ANPAHP.step_status1 = True
                ANPAHP.save()
                return redirect('myANPAHPStep2', pk = ANPAHP.pk)
        
    return render(request, 'ANPAHP/steps/ANPAHPStep1.html', content)

