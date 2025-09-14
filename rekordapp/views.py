from django.shortcuts import render
from django.http import HttpResponse
from .forms import organizationForm

# Create your views here.

def login(request):
    if request.method=="POST":
        form=organizationForm(request.POST or None)
        if form.is_valid:
            form.save()
            return render(request,"login.html")
        else:
            return render(request,"login.html")
    return render(request,"login.html")
def signup(request):
    return render(request,"signup.html")