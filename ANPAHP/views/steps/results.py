from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd

from ...models import Evaluation
from ...utils import anp
from ...utils import charts

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
    
    # Extract useful information for the report.
    # 1st: How the BSC perspective affect the overall strategy:
    bsc_families_selected = [key for key, value in ANPAHP.bsc_preferences.items() if value != 0]
    nb_families = len(bsc_families_selected)
    bsc_families_excluded = [key for key, value in ANPAHP.bsc_preferences.items() if value == 0]
    nb_families_excluded = len(bsc_families_excluded)
    
    insights = []
    
    bsc_weights = supermatrix[0][1: 1 + nb_families] + [0] * nb_families_excluded
    rounded_weights = [round(x, 4) for x in bsc_weights]
    bsc_keys = keys[1: 1 + nb_families] + bsc_families_excluded
    table_content = sorted([(key, weight) for key, weight in zip(bsc_keys, rounded_weights)])
    html_table = pd.DataFrame(table_content, columns = ["BSC Perspective", "Weight"]).transpose().to_html(index=True, header=False, classes='table table-striped')
    
    strat_insight_BSC = {
        "title": f"Balance Scorecard preferences for \"{ANPAHP.name}\"",
        "description": "Here is how important each Balance Scorecard (BSC) perspective is for your strategy:",
        "html_table": html_table,
        "graph": charts.make_radar_chart(bsc_weights, bsc_keys, ANPAHP.name),
        "extra": "Simply multiply by 100 to get percentages.",
    }
    insights.append(strat_insight_BSC)

    # 2nd: How each KPI/metric affect the overall strategy and BSC families:
    weights = [round(x, 4) for x in limiting_matrix[0][1 + nb_families:]]
    df = pd.DataFrame(weights, index=keys[1 + nb_families:])
    html_table = df.to_html(classes='table table-striped', header=False)
    
    description = (
        "Taking into account the following:" +
        "<ul>" +
        "<li>Your preferences in terms of BSC perspectives; </li>" +
        "<li>Your preferences in terms of how much each KPI/metric affects each BSC perspective;</li>" +
        "<li>Metrics dependencies as defined by you;" +
        "</ul>" +
        f"Here is how KPIs/metrics affect your overall strategy \"{ANPAHP.name}\":"
    )
    
    strat_insight_metrics = {
        "title": f"KPIs/metrics importance for \"{ANPAHP.name}\"",
        "description": description,
        "html_table": html_table,
        "graph": charts.make_radar_chart(weights, keys[1 + nb_families:], ANPAHP.name),
        "extra": "Due to a convergence process with rounding at the end, some very low priority metrics may end up with 0 importance.\n Simply multiply by 100 to get percentages.",
    }
    insights.append(strat_insight_metrics)

    # 3nd: for each BSC perspective, how much the metrics affect them:
    # TODO: Add a section for each BSC with important metrics (filter out the 0s)
    #       and the graph associated with it.
    
    # Finally, for each metric that depends on others, do the same again.
    
    # Add the PDF download thingy:
    

    
    content = {
        'ANPAHP': ANPAHP, 
        'keys': keys, 
        'supermatrix': supermatrix,
        'limiting_matrix': limiting_matrix,
        'insights': insights,
    }
    
    return render(request, 'ANPAHP/steps/ANPAHPResults.html', content)
    
    
# -----------------------------------------------------------------------------
# Results downloading views:




