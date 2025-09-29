from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from rekordapp.models import organization
from .models import event
from .forms import createeventForm
# Create your views here.

def homepage(request):
    #fetching organization details
    organizationid=request.session.get("currentorganizationid")
    organizationdetails=organization.objects.get(id=organizationid)     #use .get if you want to get only 1 result

    #fetching event details
    eventdetails=event.objects.filter(organizationid=organizationid)
    for i in eventdetails:
        print(i.eventicon.url)

    if request.method=="POST":
        action=request.POST.get("action") #for pinpointing which button was clicked
        if action=="create-event":
            form=createeventForm(request.POST, request.FILES)
            print(form)
            if form.is_valid():
                print("DATA:",form.cleaned_data)
                form.save()
                messages.success(request, "Data Added successfully!")
            else:
                print("BUTTON WORKS BUT SOME FORM ERROR")

    return render(request,"homepage.html",{"orgdetails":organizationdetails,"events":eventdetails})