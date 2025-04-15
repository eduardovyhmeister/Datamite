from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..helpers import slug_equal
from ...forms import BSCPreferencesForm
from ...models import Evaluation, BSCFamily


@login_required
def step2_view(request, pk):
    ANPAHP = Evaluation.objects.get(pk = pk)
    
    if request.method == 'POST':
        print("POST DATA:", request.POST)
        form = BSCPreferencesForm(request.POST)
        if form.is_valid():
            preferences = {}
            # Extract preferences properly by matching names:
            # Necessary because JS doesn't like non-slug names.
            for family in BSCFamily.objects.all():
                for slug_name, value in form.cleaned_data.items():
                    if slug_equal(family.name, slug_name):
                        preferences[family.name] = value
                        continue
            
            print(preferences)
            # Save those preferences and compute the matrix of preferences.
            # TODO: Compute the matrix of preferences.
            # Redirect to step 3
            # Update step 2 status
            return render(request, 'ANPAHP/steps/ANPAHPStep2.html', {
                'form': form,
                'ANPAHP': ANPAHP,
                'subfamilies': BSCFamily.objects.all(),
            })
    else:
        form = BSCPreferencesForm()

    return render(request, 'ANPAHP/steps/ANPAHPStep2.html', {
        'form': form,
        'ANPAHP': ANPAHP,
        'subfamilies': BSCFamily.objects.all(),
    })
