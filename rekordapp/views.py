from django.shortcuts import render
from django.http import HttpResponse
from .forms import signupForm,loginForm
from .models import organization
from django.contrib import messages

# Create your views here.

#LOGIN FUNCTION
def login(request):
    if request.method=="POST":
        form=loginForm(request.POST or None) #takes all the values submitted and makes it into a form
        if form.is_valid():   #checks if all fields are filled out 
            loginemail=form.cleaned_data["loginemail"]      #cleaned_data is used to get only the data and remove the entire form structure
            loginpassword=form.cleaned_data["loginpassword"]
            try:
                currentorganization=organization.objects.get(email=loginemail,password=loginpassword) #checks if user exists in database
                request.session["currentorganizationid"]=currentorganization.id     #store the organization id in a session
                print(currentorganization)
                request.session["currentorganizationid"]=currentorganization.id     #saving organization id in session
                messages.success(request, "Login successful!")
            except:
                 messages.error(request, "Invalid Credentials!")
    return render(request,"login.html")


def signup(request):
    if request.method=="POST":
        form=signupForm(request.POST or None)
        print("Form Recieved")
        print(form)
        if form.is_valid():
            form.save()
            messages.success(request, "Signup successful!")
        else:
            messages.error(request, "An error occured while creating your account.This could be due to any faulty data provided. Please verify and re-enter your data")

    return render(request,"signup.html")