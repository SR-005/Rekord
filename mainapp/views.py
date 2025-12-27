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
from .reporthandler import main as reporthandler
import secrets
import string
import uuid
import io

#---------------------------------------------------------------USER DEFINED----------------------------------------------------------------

#to rename file and saving them and editing image for nft 
def filemanipulate(file,trigger,organizationname,lasteventid):

    if trigger==0:                          #trigger=0: csv, rename file and specify path accordingly
        defaultpath="reports/"
        extension=".csv"
    else:                                   #trigger=1: image, rename file and specify path accordingly
        defaultpath="icons/"
        extension=".png"

    currenteventid=lasteventid+1                    #match name with eventid
    filename=str(organizationname)+str(currenteventid)+extension      #generate custom img name: orgname+eventid
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

#to generate password for authenticating claim links
def generatepassword():
    length=8
    alphabet=string.ascii_lowercase+string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))

#to geneate tokens and unique claim links
def generatetokens(request,lasteventobject,name,email):
    uniquetoken=str(uuid.uuid4())               #generate unique tokens for each participants
    claimurl = request.build_absolute_uri(reverse("claim", kwargs={"code": uniquetoken}))   #building claim urls with token
    password=generatepassword() #call function to generate password

    eventtoken.objects.create(eventid=lasteventobject,name=name,email=email,claimurl=claimurl,claimpass=password)        #adding tokens in association with emails and event

#---------------------------------------------------------------HTML FUNCTIONS----------------------------------------------------------------

def homepage(request):
    #fetching organization details
    organizationid=request.session.get("currentorganizationid")
    organizationdetails=organization.objects.get(id=organizationid)     #use .get if you want to get only 1 result

    #fetching event details
    eventdetails=event.objects.filter(organizationid=organizationid)

    return render(request,"homepage.html",{"orgdetails":organizationdetails,"events":eventdetails})

def create(request):
    formnumber = None           #number of participants in a physical event
    lasteventid=None            
    eventtype=None              #virtual or physical
    vparticipants=None
    count=None
    
    #fetching organization details
    organizationid=request.session.get("currentorganizationid")
    organizationdetails=organization.objects.get(id=organizationid)     #use .get if you want to get only 1 result
    

    #fetching event details
    eventdetails=event.objects.filter(organizationid=organizationid)

    if request.method=="POST":
        action=request.POST.get("action") #for pinpointing which button was clicked
        if action=="create-event":
            form=createeventForm(request.POST, request.FILES)

            '''print("----EVENT FORM----")
            print(form)'''

            if form.is_valid():
                print("DATA:",form.cleaned_data)
                eventobject=form.save(commit=False)         #commit=Flase: means data will not be saved to db
                
                #fetching last event id
                try:
                    lasteventdetails=event.objects.last()   #used for fetching last created row(in order to get the eventid)
                    lasteventid=lasteventdetails.eventid        #event id of the previous event(+1 for the current event id)
                    print("Last Event ID: ",lasteventid)
                except:
                    lasteventid=0
                    print("This is the First Event")

                try: 
                    formnumber=request.POST.get("eventparticipants")
                except:
                    print("No Event Participants Found: Not a Physical Event")

                #csv and img fetching: from create event form
                eventtype=request.POST.get("eventtype")
                print("Current Event Type: ", eventtype)
                file=request.FILES.get("eventreport")
                image=request.FILES.get("eventicon")

                if image:
                    #file renaming: if virtual (if not physical)
                    if eventtype=="virtual":
                        filepath=filemanipulate(file,0,organizationdetails.name,lasteventid)       #if trigger=0: file
                        eventobject.eventreport=filepath

                    imagepath=filemanipulate(image,1,organizationdetails.name,lasteventid)      #if trigger=1: image
                    eventobject.eventicon=imagepath
                    eventobject.save()
                messages.success(request, "Event Added successfully!")

            else:
                print("BUTTON WORKS BUT SOME FORM ERROR")

            if eventtype=="virtual":
                vparticipants,count=reporthandler(filepath)
                vnames=list(vparticipants.keys())
                vparticipantemails=list(vparticipants.values())

                lasteventobject=event.objects.get(eventid=lasteventid)

                for i,vmail in enumerate(vparticipantemails):
                    print("Name: ",vnames[i])
                    print("Email: ",vmail)
                    print("\n")
                    generatetokens(request,lasteventobject,vnames[i],vmail)           #calls token generating function

            
            lasteventdetails=event.objects.last()   #used for fetching last created row(in order to get the eventid)
            lasteventid=lasteventdetails.eventid        #event id of the previous event(+1 for the current event id)
            #lasteventid=lasteventid+1           #increment: added current event
            request.session["lasteventid"]=lasteventid  #saving latest event id in session
            

        if action=="physical-generate":             #Generates Token: (as next step if event is physical event)
            print("ENTERED THE GENERATE TOKENS FUNCTION")

            lasteventid=request.session.get("lasteventid")          
            print("Current Event ID: ",lasteventid)
            lasteventobject=event.objects.get(eventid=lasteventid)
            
            pname=request.POST.getlist("name")
            pparticipantemails=request.POST.getlist("emails")        #fetching entered email from form
            print("List of Emails: ", pparticipantemails)

            for i,pmail in enumerate(pparticipantemails):
                print("Name: ",pname[i])
                print("Email: ",pmail)
                print("\n")
                generatetokens(request,lasteventobject,pname[i],pmail)           #calls token generating function

            messages.success(request, "Tokens generated successfully!")
            return redirect("homepage")
        
    return render(request, "create.html",{"orgdetails":organizationdetails,"events":eventdetails,"formnumber":formnumber})

def claim(request,code):
    
    url="http://127.0.0.1:8000/claim/"+code+"/"

    claimtokenobject=eventtoken.objects.get(claimurl=url)
    name=claimtokenobject.name
    print("Name: ",name)
    claimeventobject=claimtokenobject.eventid

    return render(request,"claim.html",{"event":claimeventobject,"claimtoken":claimtokenobject})