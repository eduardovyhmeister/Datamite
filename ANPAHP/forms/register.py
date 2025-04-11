from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegisterForm(UserCreationForm):
    """Form used to register a new 'User' into the system."""
    
    class Meta:
        model = User
        fields = ('username','email','password1','password2',)
        widgets = {
            'username' : forms.TextInput(attrs={'class':'input'}),
            'email' : forms.EmailInput(attrs={'class':'input'}),
            'password1' : forms.PasswordInput(attrs={'class':'input'}),
            'password2' : forms.PasswordInput(attrs={'class':'input'}),
        }