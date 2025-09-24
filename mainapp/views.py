from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from rekordapp.models import organization
# Create your views here.

def homepage(request):
    organizationid=request.session.get("currentorganizationid")
    organizationdetails=organization.objects.get(id=organizationid)
    print(organizationdetails.id,organizationdetails.name)
    return render(request,"homepage.html",{"organizationname":organizationdetails.name})
