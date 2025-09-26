from django import forms
from .models import events

class createeventForm(forms.ModelForm):
    class Meta:
        model=events
        fields=["eventname", "eventdescription", "city","eventdate","eventicon"]
