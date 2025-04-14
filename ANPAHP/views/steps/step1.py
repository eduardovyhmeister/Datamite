from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ...models import Evaluation, Objective
from ...forms import ObjectiveSelectionForm

@login_required
def step1_view(request, pk):
    ANPAHP = Evaluation.objects.get(pk = pk)
    form = ObjectiveSelectionForm(request.POST or None, instance = ANPAHP)
    
    content = {'ANPAHP': ANPAHP,
               'form': ObjectiveSelectionForm(request.POST or None, 
                                              instance = ANPAHP),
               }
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return render(request, 'ANPAHP/ANPAHPStep1.html', content)
        # TODO: return redirect('myANPAHPStep2', pk = ANPAHP.pk)
        
    return render(request, 'ANPAHP/ANPAHPStep1.html', content)

