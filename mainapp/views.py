from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from rekordapp.models import organization
from .forms import createeventForm
# Create your views here.

def homepage(request):
    organizationid=request.session.get("currentorganizationid")
    organizationdetails=organization.objects.get(id=organizationid)

    if request.method=="POST":
        action=request.POST.get("action") #for pinpointing which button was clicked
        if action=="create-event":
            form=createeventForm(request.POST, request.FILES)
            '''print(form)'''
            if form.is_valid():
                print("DATA:",form.cleaned_data)
            else:
                print("BUTTON WORKS BUT SOME FORM ERROR")
    return render(request,"homepage.html",{"organizationname":organizationdetails.name, "organizationemail":organizationdetails.email})
