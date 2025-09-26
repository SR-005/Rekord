from django.db import models
from django.contrib.auth.models import User
from rekordapp.models import organization

# Create your models here.
class events(models.Model):
    eventid=models.AutoField(primary_key=True)
    organizationid=models.ForeignKey(organization, on_delete=models.CASCADE,related_name="events") #use event.organization.fieldname to access foreign table data
    eventname=models.CharField(max_length=100)
    eventdescription=models.CharField(max_length=200)
    city=models.CharField(max_length=20)
    eventdate=models.CharField(max_length=12)
    #for saving icons. it doesnt save icon as img, it will automatically save it to /media/icons and only save it path in db.
    #use 'event.eventicon.url' to access it
    eventicon = models.ImageField(upload_to="icons/")
    def __str__(self):
        return self.eventname