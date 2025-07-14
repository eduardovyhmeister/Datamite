"""Module for views concerning the management of ANP-AHP Evaluations (see,
create, delete)."""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from ..models import Evaluation
from ..forms import ANPAHPForm


@login_required
def my_anp_ahp(request):
    """Main page where you can create new ANP-AHP Evaluations and manage them."""
    ANPAHPs = Evaluation.objects.all().filter(author = request.user)
    context = {'ANPAHPs': ANPAHPs}
    return render(request,'ANPAHP/myANPAHP.html', context)
 

@login_required
def my_anp_ahp_create(request):
    """Page used to create a new AHP-ANP Evaluation."""
    submitted = False
    if request.method == "POST":
        form = ANPAHPForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit = False) # this create the form but do not commit it so can be modified
            assessment.author = request.user # modify the form
            assessment.save()
            # Redirect to the newly created Evaluation:
            # print(assessment)
            ANPAHP = Evaluation.objects.get(author = request.user, name = assessment.name)
            return redirect('myANPAHPHome', pk = ANPAHP.pk)
            # Stay on the same page with the newly created evaluation:
            # return HttpResponseRedirect('myANPAHP') # /add_event?submitted=True
    else:
        form = ANPAHPForm
        if 'submitted' in request.GET:
            submitted = True
    form = ANPAHPForm
    return render(request, 'ANPAHP/myANPAHPCreate.html', {'form': form, 'submitted': submitted})


@login_required
def my_anp_ahp_delete(request, pk):
    """Called when cliking on delete an ANP-AHP Evaluation, deletes it from the DB."""
    anpahp = Evaluation.objects.get(pk = pk)
    anpahp.delete()
    return redirect('myANPAHP')