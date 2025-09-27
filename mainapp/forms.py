from django import forms
from .models import event

class createeventForm(forms.ModelForm):
    class Meta:
        model=event
        fields=["organizationid","eventname", "eventdescription", "city","eventdate","eventicon"]
