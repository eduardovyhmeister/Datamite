"""Module for basic views: basic website pages such as home, about, etc.
Basically any page you can find directly in the header."""

from django.shortcuts import render


# -----------------------------------------------------------------------------
# Basic pages:

def home(request):
    """View for the homepage."""
    return render(request, 'home.html')


def how_to_anp_ahp_view(request):
    """View for the How To page about ANP-AHP."""
    return render(request, 'howto_ANP_AHP.html')


def about_view(request):
    """View for the 'about' page."""
    return render(request, 'about.html')



