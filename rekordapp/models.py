from django.db import models
from django.contrib.auth.models import User 

# Create your models here.
class organization(models.Model):
    id=models.AutoField(primary_key=True)   #automatic id
    name=models.CharField(max_length=100,unique=True)   #name of the organization   
    email=models.EmailField(unique=True)   #email of the organization
    password=models.CharField(max_length=30)    #passoword

def __str__(self):
    return self.name