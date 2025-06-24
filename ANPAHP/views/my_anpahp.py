from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Evaluation
from ..forms import NotesForm

@login_required
def my_anpahp_home_view(request, pk):
    """View used to show the home of a ANP-AHP process."""
    ANPAHP = Evaluation.objects.get(pk = pk)
    form = NotesForm(request.POST or None, instance = ANPAHP)
    content = {'ANPAHP': ANPAHP,
               'form': form}
    
    if form.is_valid():
        form.save()
        # return render(request, 'ANPAHP/ANPAHPHome.html', content)
        return redirect('myANPAHPStep1', pk = ANPAHP.pk)
    
    return render(request, 'ANPAHP/ANPAHPHome.html', content)
