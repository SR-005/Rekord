from django import forms
from .models import organization

class signupForm(forms.ModelForm):
    class Meta:
        model=organization
        fields=["name", "email", "password"]    #db fields

class loginForm(forms.Form):
    loginemail = forms.EmailField()
    loginpassword = forms.CharField(widget=forms.PasswordInput)