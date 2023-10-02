from django.db import models
# Create your models here.
class Userdetails(models.Model):
    GuestFullName=models.CharField(max_length=50)
    Email=models.CharField(max_length=100)
    PhoneNumber=models.CharField(max_length=10)
    AdditionalInformation=models.CharField(max_length=200)