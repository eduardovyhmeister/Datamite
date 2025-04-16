"""Module for views used in creating/deleting objectives, criteria, and KPIs."""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..models import Evaluation, Objective, Criterion, KPI
from ..forms import (CreateObjectiveForm, 
                     DeleteObjectiveForm,
                     CreateKPIForm,
                     DeleteKPIForm,)


# -----------------------------------------------------------------------------
# Objective management:

@login_required
def create_objective_view(request, pk):
    """View used in creating a new objective.
    
    Args:
        pk (any): The primary key of the Evaluation model. Used for
            redirecting the user to the right page after the objective
            has been created successfully.
    """
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    if request.method == "POST":
        form = CreateObjectiveForm(request.POST)
        if form.is_valid():
            objective = form.save(commit = False) # this create the objective but does not commit it so can be modified
            objective.author = request.user # modify the form
            objective.save()
            return redirect('myANPAHPStep1', pk = pk) # Return to the objective selection step
    else:
        form = CreateObjectiveForm()
        
    return render(request,'ANPAHP/new_objective.html',{'form': form,
                                                       'ANPAHP': ANPAHP})
    

@login_required
def delete_objective_view(request, pk):
    """View to delete one of the user's objectives by selecting from a list.
    
    Args:
        pk (any): The primary key of the Evaluation model. Used for
            redirecting the user to the right page after the objective
            has been deleted successfully.
    """
    ANPAHP = Evaluation.objects.get(pk = pk)

    if request.method == 'POST':
        form = DeleteObjectiveForm(request.POST)
        form.fields['objective'].queryset = Objective.objects.filter(author = request.user)
        if form.is_valid():
            objective = form.cleaned_data['objective']
            objective.delete()
            return redirect('myANPAHPStep1', pk = pk)
    else:
        form = DeleteObjectiveForm()
        form.fields['objective'].queryset = Objective.objects.filter(author = request.user)

    content = {'form': form, 'ANPAHP': ANPAHP}
    return render(request, 'ANPAHP/delete_objective.html', content)


# -----------------------------------------------------------------------------
# KPIs management:

@login_required
def create_kpi_view(request, pk):
    """View used in creating a new KPI.
    
    Args:
        pk (any): The primary key of the Evaluation model. Used for
            redirecting the user to the right page after the KPI
            has been created successfully.
    """
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    if request.method == "POST":
        form = CreateKPIForm(request.POST)
        if form.is_valid():
            kpi = form.save(commit=False)
            kpi.author = request.user
            kpi.save()
            form.save_m2m()  # Save M2M field
            return redirect('myANPAHPStep3', pk = pk) # Return to the KPI selection step
    else:
        form = CreateKPIForm()
        
    return render(request,'ANPAHP/new_kpi.html', {'form': form,
                                                  'ANPAHP': ANPAHP})
    

@login_required
def delete_kpi_view(request, pk):
    """View to delete one of the user's KPIs by selecting from a list.
    
    Args:
        pk (any): The primary key of the Evaluation model. Used for
            redirecting the user to the right page after the KPI
            has been deleted successfully.
    """
    ANPAHP = Evaluation.objects.get(pk = pk)

    if request.method == 'POST':
        form = DeleteKPIForm(request.POST)
        form.fields['kpi'].queryset = KPI.objects.filter(author = request.user)
        if form.is_valid():
            kpi = form.cleaned_data['kpi']
            kpi.delete()
            return redirect('myANPAHPStep3', pk = pk)
    else:
        form = DeleteKPIForm()
        form.fields['kpi'].queryset = KPI.objects.filter(author = request.user)

    content = {'form': form, 'ANPAHP': ANPAHP}
    return render(request, 'ANPAHP/delete_kpi.html', content)


# -----------------------------------------------------------------------------
# Criteria management:
