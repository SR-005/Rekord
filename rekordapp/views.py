from django.shortcuts import render
from django.http import HttpResponse
from .forms import organizationForm,loginForm
from .models import organization
from django.contrib import messages

# Create your views here.

#LOGIN FUNCTION
def login(request):
    if request.method=="POST":
        form=loginForm(request.POST or None) #takes all the values submitted and makes it into a form
        if form.is_valid():   #checks if all fields are filled out 
            email=form.cleaned_data["loginemail"]
            password=form.cleaned_data["loginpassword"]
            try:
                currentorganization=organization.objects.get(email=email,password=password) #checks if user exists in database
                request.session["currentorganizationid"]=currentorganization.id     #store the organization id in a session
                print(currentorganization)
            except:
                 print("Invalid Credentials")
    return render(request,"login.html")
def signup(request):
    return render(request,"signup.html")