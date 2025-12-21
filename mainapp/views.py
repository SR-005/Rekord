from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from rekordapp.models import organization
from .models import event,eventtoken
from .forms import createeventForm,generatelinksForm
from .imagemal import imagemanipulation
import uuid
import io

#---------------------------------------------------------------USER DEFINED----------------------------------------------------------------

def filemanipulate(file,trigger,organizationname,lasteventid):

    if trigger==0:
        defaultpath="reports/"
        extension=".csv"
    else:
        defaultpath="icons"
        extension=".png"

    currenteventid=lasteventid+1                    #match name with eventid
    filename=str(organizationname)+str(currenteventid)+extension      #generate custom img name: orgname+eventid
    print("Image Name: ",filename)
    path=defaultpath+filename                      #generate path

    if trigger==0:          #save csv to path
        filesavedpath=default_storage.save(path,ContentFile(file.read()))
        return filesavedpath

    else:                   #save image to path
        image=imagemanipulation(file)              #function call for image manipulation

        #getting img from pil return type
        buffer=io.BytesIO()         
        image.save(buffer, format="PNG")
        buffer.seek(0)

        imgsavedpath=default_storage.save(path,ContentFile(buffer.read()))         #saving img to actual output path: media/icons/..
        return imgsavedpath



#---------------------------------------------------------------HTML FUNCTIONS----------------------------------------------------------------

def homepage(request):
    formnumber = None
    lasteventid=None
    
    #fetching organization details
    organizationid=request.session.get("currentorganizationid")
    organizationdetails=organization.objects.get(id=organizationid)     #use .get if you want to get only 1 result
    

    #fetching event details
    eventdetails=event.objects.filter(organizationid=organizationid)

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

                

                #csv and img fetching: from create event form
                file=request.FILES.get("eventreport")
                image=request.FILES.get("eventicon")

                if image:
                    filepath=filemanipulate(file,0,organizationdetails.name,lasteventid)       #if trigger=0: file
                    eventobject.eventreport=filepath

                    imagepath=filemanipulate(image,1,organizationdetails.name,lasteventid)      #if trigger=1: image
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