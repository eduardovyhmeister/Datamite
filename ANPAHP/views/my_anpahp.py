from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Evaluation
from ..forms import NotesForm

@login_required
def my_anpahp_home_view(request, pk):
    ANPAHP = Evaluation.objects.get(pk = pk)
    form = NotesForm(request.POST or None, instance = ANPAHP)
    if form.is_valid():
        form.save()
        return render(request, 'ANPAHP/ANPAHPHome.html',{'ANPAHP': ANPAHP, 'form': form})
    return render(request, 'ANPAHP/ANPAHPHome.html',{'ANPAHP': ANPAHP, 'form': form})
