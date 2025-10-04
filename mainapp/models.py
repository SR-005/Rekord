from django.db import models
from django.contrib.auth.models import User
from rekordapp.models import organization

# Create your models here.
class event(models.Model):
    eventid=models.AutoField(primary_key=True)
    organizationid=models.ForeignKey(organization, on_delete=models.CASCADE,related_name="event") #use event.organization.fieldname to access foreign table data
    eventname=models.CharField(max_length=100)
    eventdescription=models.CharField(max_length=200)
    city=models.CharField(max_length=20)
    eventdate=models.CharField(max_length=12)
    eventtype=models.CharField(max_length=20)
    eventreport = models.FileField(upload_to="reports/", null=True, blank=True)  # goes to media/reports/
    eventparticipants = models.IntegerField(null=True, blank=True) 
    #for saving icons. it doesnt save icon as img, it will automatically save it to /media/icons and only save it path in db.
    #use 'event.eventicon.url' to access it
    eventicon = models.ImageField(upload_to="icons/")
    def __str__(self):
        return self.eventname
    
class eventtoken(models.Model):
    tokenid=models.AutoField(primary_key=True)
    eventid=models.ForeignKey(event, on_delete=models.CASCADE,related_name="eventtoken")
    email=models.EmailField()
    token=models.CharField(max_length=100)
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return self.tokenid