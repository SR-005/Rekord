from django import forms
from models import organization

class organizationForm(forms.ModelForm):
    class Meta:
        model=organization
        fields=["name","email","password"]