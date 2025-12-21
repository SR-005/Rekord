from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rekordapp.models import organization
from .models import event,eventtoken
from .forms import createeventForm,generatelinksForm
import uuid
import os

# Create your views here.
def saveimage(image,organizationname,lasteventid):
    currenteventid=lasteventid+1
    extention=image.name.split('.')[-1]
    imagename=str(organizationname)+str(currenteventid)+"."+extention
    print("Image Name: ",imagename)

    path=os.path.join("icons/",imagename)
    savedpath=default_storage.save(path,ContentFile(image.read()))
    return savedpath


def homepage(request):
    formnumber = None
    lasteventid=None
    
    #fetching organization details
    organizationid=request.session.get("currentorganizationid")
    organizationdetails=organization.objects.get(id=organizationid)     #use .get if you want to get only 1 result
    eventcount=organization.objects.filter(id=organizationid).count()
    print("Event Count: ",eventcount)
    

    #fetching event details
    eventdetails=event.objects.filter(organizationid=organizationid)
    for i in eventdetails:
        print(i.eventicon.url)

    if request.method=="POST":
        action=request.POST.get("action") #for pinpointing which button was clicked
        if action=="create-event":
            form=createeventForm(request.POST, request.FILES)
            print("----EVENT FORM----")
            print(form)
            if form.is_valid():
                print("DATA:",form.cleaned_data)
                eventobject=form.save(commit=False)         #commit=Flase: means data will not be saved to db
                lasteventdetails=event.objects.last()   #used for fetching last created row(in order to get the eventid)
                lasteventid=lasteventdetails.eventid        #event id of the previous event(+1 for the current event id)
                print("Last Event ID: ",lasteventid)

                image=request.FILES.get("eventicon")
                if image:
                    imagepath=saveimage(image,organizationdetails.name,lasteventid)
                    eventobject.eventicon=imagepath
                    eventobject.save()
                messages.success(request, "Event Added successfully!")
            else:
                print("BUTTON WORKS BUT SOME FORM ERROR")
            
            lasteventdetails=event.objects.last()   #used for fetching last created row
            print("Event Type: ",lasteventdetails.eventtype)
            if lasteventdetails.eventtype=="physical":
                formnumber=lasteventdetails.eventparticipants
                lasteventid=lasteventdetails.eventid

            request.session["lasteventid"]=lasteventid  #saving latest event id in session

        elif action=="generate-tokens":
            lasteventid=request.session.get("lasteventid")
            lasteventobject = event.objects.get(eventid=lasteventid)
            participantemails=request.POST.getlist("emails")
            
            print(lasteventid)

            for email in participantemails:
                uniquetoken=str(uuid.uuid4())
                claimurl = request.build_absolute_uri(reverse("claim", kwargs={"code": uniquetoken}))
                eventtoken.objects.create(eventid=lasteventobject,email=email,claimurl=claimurl)
            messages.success(request, "Tokens generated successfully!")
            return redirect("homepage")


    return render(request,"homepage.html",{"orgdetails":organizationdetails,"events":eventdetails,"formnumber":formnumber})

def claim(request,code):
    return HttpResponse(f"Connected Successfully")