from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.http import HttpResponse
import pandas as pd
from xhtml2pdf import pisa

from ...models import Evaluation
from ...utils import anp
from ...utils import charts


# -----------------------------------------------------------------------------
# Views:


@login_required
def results_view(request, pk):
    """View for the results of the ANP-AHP analysis once everything has been
    completed. Will generate the supermatrix and compute its limiting matrix.
    No form in this view, simply display data.
    """
    ANPAHP = Evaluation.objects.get(pk = pk)
    keys, supermatrix, limiting_matrix, insights = extract_insights(ANPAHP)
    
    context = {
        'ANPAHP': ANPAHP, 
        'keys': keys, 
        'supermatrix': supermatrix,
        'limiting_matrix': limiting_matrix,
        'insights': insights,
    }
    
    return render(request, 'ANPAHP/steps/ANPAHPResults.html', context)
    

@login_required
def download_pdf_report(request, pk):
    """View used to generate and download the PDF report."""
    ANPAHP = Evaluation.objects.get(pk = pk)
    keys, supermatrix, limiting_matrix, insights = extract_insights(ANPAHP)
    
    context = {
        'ANPAHP': ANPAHP, 
        'keys': keys, 
        'supermatrix': supermatrix,
        'limiting_matrix': limiting_matrix,
        'insights': insights,
    }
    
    # Build a PDF response:
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{ANPAHP.name} - ANP-AHP Report.pdf"'
    
    # Use an HTML template to generate the report:
    html = get_template("ANPAHP/steps/ANPAHPReport.html").render(context)
    pisa.CreatePDF(html, dest=response)
    return response

    
# -----------------------------------------------------------------------------
# Utility functions:


def extract_insights(evaluation, pie_chart_threshold=0.02):
    """Extract the insights from the ANP-AHP process for the provided evaluation.
    
    Given an evaluation, the supermatrix, the limiting matrix, and the insights
    we can extract from these matrices are computed/provided. The insights are
    formatted as a list of dictionaries, each dictionary representing a subsection
    of the report to be generated for the user.
    The insights may have the following keys:
     - "title": A title for your section.
     - "description": A description for the section, a short text to explain what
                      we are presenting in this section.
     - "html_table": A readily-formatted table to be displayed (using `|safe`) of
                     the insight.
     - "graph": A readily-formatted graph to be displayed (using `|safe`) of the
                insight.
     - "extra": A piece of text to be added, for instance as a note to the figure
                or the table.
    
    Args:
        evaluation (models.Evaluation): The completed Evaluation to extract the
            insights for.
            
    Returns:
        (list[str], list[list[value]], list[list[value]], list[dict[str: obj]]) -
        1) The keys used for the matrices/tables, in the right order.
        2) The supermatrix built from the completed evaluation.
        3) The limiting supermatrix computed from the supermatrix.
        4) A list of insights in the form of a dictionary of content to be used
           in the HTML template.
    """
    keys, supermatrix = anp.build_supermatrix(evaluation.bsc_preferences, 
                                              evaluation.kpis_preferences,
                                              evaluation.intermetric_preferences)
    limiting_matrix = anp.compute_limiting_matrix(supermatrix)
    
    # Extract useful information for the report.
    # 1st: How the BSC perspective affect the overall strategy:
    bsc_families_selected = [key for key, value in evaluation.bsc_preferences.items() if value != 0]
    nb_families = len(bsc_families_selected)
    bsc_families_excluded = [key for key, value in evaluation.bsc_preferences.items() if value == 0]
    nb_families_excluded = len(bsc_families_excluded)
    
    insights = []
    
    bsc_weights = supermatrix[0][1: 1 + nb_families] + [0] * nb_families_excluded
    rounded_weights = [round(x, 4) for x in bsc_weights]
    bsc_keys = keys[1: 1 + nb_families] + bsc_families_excluded
    table_content = sorted([(key, weight) for key, weight in zip(bsc_keys, rounded_weights)])
    html_table = pd.DataFrame(table_content, columns = ["BSC Perspective", "Weight"]).transpose().to_html(index=True, header=False, classes='table table-striped')
    
    strat_insight_BSC = {
        "title": f"Balance Scorecard preferences for \"{evaluation.name}\"",
        "description": "Here is how important each Balance Scorecard (BSC) perspective is for your strategy:",
        "html_table": html_table,
        "graph": charts.make_pie_chart(bsc_weights, bsc_keys, evaluation.name),
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
        f"Here is how KPIs/metrics affect your overall strategy \"{evaluation.name}\":"
    )
    
    strat_insight_metrics = {
        "title": f"KPIs/metrics importance for \"{evaluation.name}\"",
        "description": description,
        "html_table": html_table,
        "graph": charts.make_pie_chart(weights, keys[1 + nb_families:], evaluation.name, threshold=pie_chart_threshold),
        "extra": "Due to a convergence process with rounding at the end, some very low priority metrics may end up with 0 importance.\n Simply multiply by 100 to get percentages.",
    }
    insights.append(strat_insight_metrics)

    # 3nd: for each BSC perspective, how much the metrics affect them:
    for i, bsc_family in enumerate(bsc_families_selected):
        weights = [round(x, 4) for x in limiting_matrix[1+i][1 + nb_families:]]
        df = pd.DataFrame(weights, index=keys[1 + nb_families:])
        html_table = df.to_html(classes='table table-striped', header=False)
        
        description = (
            "Taking into account the following:" +
            "<ul>" +
            "<li>Your preferences in terms of how much each KPI/metric affects each BSC perspective;</li>" +
            "<li>Metrics dependencies as defined by you;" +
            "</ul>" +
            f"Here is how KPIs/metrics affect the {bsc_family}:"
        )
        
        strat_insight_metrics = {
            "title": f"KPIs/metrics importance for the {bsc_family}",
            "description": description,
            "html_table": html_table,
            "graph": charts.make_pie_chart(weights, keys[1 + nb_families:], f"KPIs/metrics contribution to the {bsc_family}", threshold=pie_chart_threshold),
            "extra": "Due to a convergence process with rounding at the end, some very low priority metrics may end up with 0 importance.\n Simply multiply by 100 to get percentages.",
        }
        insights.append(strat_insight_metrics)
    
    # Finally, for each metric that depends on others, do the same again.
    for i, kpi_name in enumerate(keys[1 + nb_families:], 1 + nb_families):
        nb_dependencies = len([x for x in supermatrix[i] if x != 0])
        if nb_dependencies == 1: continue # No dependency other than itself.
        
        weights = [round(x, 4) for x in limiting_matrix[i][1 + nb_families:]]
        df = pd.DataFrame(weights, index=keys[1 + nb_families:], columns=["weight"])
        df = df[df.weight != 0] # Filter out the 0s from the list.
        html_table = df.to_html(classes='table table-striped', header=False)
        
        description = f"Taking into account all the relationships you defined between KPIs/metrics, here is how to compute \"{kpi_name}\":"
        
        strat_insight_metrics = {
            "title": f"KPIs/metrics importance for the computation of {kpi_name}",
            "description": description,
            "html_table": html_table,
            "graph": charts.make_pie_chart(weights, keys[1 + nb_families:], f"KPIs/metrics contribution to {kpi_name}", threshold=pie_chart_threshold),
            "extra": "Due to a convergence process with rounding at the end, some very low priority metrics may end up with 0 importance.\n Simply multiply by 100 to get percentages.",
        }
        insights.append(strat_insight_metrics)
    
    return (keys, supermatrix, limiting_matrix, insights)



