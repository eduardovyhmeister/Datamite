from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ...models import Evaluation
from ...utils import anp

@login_required
def results_view(request, pk):
    """View for the results of the ANP-AHP analysis once everything has been
    completed. Will generate the supermatrix and compute its limiting matrix.
    No form in this view, simply display data.
    """
    ANPAHP = Evaluation.objects.get(pk = pk)
    keys, supermatrix = anp.build_supermatrix(ANPAHP.bsc_preferences, 
                                              ANPAHP.kpis_preferences,
                                              ANPAHP.intermetric_preferences)
    limiting_matrix = anp.compute_limiting_matrix(supermatrix)
    
    content = {
        'ANPAHP': ANPAHP, 
        'keys': keys, 
        'supermatrix': supermatrix,
        'limiting_matrix': limiting_matrix,
    }
    
    return render(request, 'ANPAHP/steps/ANPAHPResults.html', content)
    
    
# -----------------------------------------------------------------------------
# Results downloading views:




