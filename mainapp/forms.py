from django import forms
from .models import event,eventtoken

class createeventForm(forms.ModelForm):
    class Meta:
        model = event
        fields = ["organizationid", "eventname", "eventdescription", "city","eventdate", "eventtype", "eventreport", "eventparticipants", "eventicon"]

    def clean(self):
        cleaned_data=super().clean()
        eventtype=cleaned_data.get("eventtype")
        report=cleaned_data.get("eventreport")
        participants=cleaned_data.get("eventparticipants")

        if eventtype=="virtual":
            if not report:
                raise forms.ValidationError("Virtual events require an event report file.")
            # clear participants field
            cleaned_data["eventparticipants"]=None  

        elif eventtype == "physical":
            if not participants:
                raise forms.ValidationError("Physical events require participant count.")
            # clear report field
            cleaned_data["eventreport"]=None  

        return cleaned_data
    
class generatelinksForm(forms.ModelForm):
    class Meta:
        model = eventtoken
        fields=["eventid","email","claimurl"]
