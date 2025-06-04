"""Module for basic views: basic website pages such as home, about, etc.
Basically any page you can find directly in the header."""

from django.shortcuts import render

from ..models import BSCFamily


# -----------------------------------------------------------------------------
# Basic pages:

def home(request):
    """View for the homepage."""
    return render(request, 'home.html')


def how_to_anp_ahp_view(request):
    """View for the How To page about ANP-AHP."""
    context = {"BSC_Families": BSCFamily.objects.all()}
    return render(request, 'howto_ANP_AHP.html', context)


def about_view(request):
    """View for the 'about' page."""
    return render(request, 'about.html')



