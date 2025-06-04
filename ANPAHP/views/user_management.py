"""Module for views concerning user management: registration, login, logout."""

from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from ..forms import RegisterForm


# -----------------------------------------------------------------------------
# User management:

def user_register_view(request):
    """View used to provide the form and the context necessary when registering
    a new 'User'."""
    form = RegisterForm

    if request.method == 'POST': 
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Account was created for ' + user)
            return redirect('login')
    
    context = {'form' : form}
    return render(request,'registration.html', context)


def user_login_view(request):
    """View used to provide the form required for a user to log in."""
    if request.method =="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        user = authenticate(request, username = username,
                            password = password)

        if user is not None:
            login(request, user)
            return redirect('home') 
            # TODO: Redirect to the page before login was clicked.
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request,'login.html', context)


def user_logout_view(request):
    """Called when clicking 'logout' in the header."""
    logout(request)
    # Redirect to the same page or HOME if it was a user-specific page:
    referer = request.META.get('HTTP_REFERER')
    if "Not Found" in str(referer) or "myANPAHP" in str(referer):
        return redirect('home')
    else:
        return redirect(referer)


