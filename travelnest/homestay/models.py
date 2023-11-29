from django.db import models
# Create your models here.
class Userdetails(models.Model):
    GuestFullName=models.CharField(max_length=50)
    Email=models.CharField(max_length=100)
    PhoneNumber=models.CharField(max_length=10)
    AdditionalInformation=models.CharField(max_length=200)


class Payment(models.Model):
    GuestFullName = models.ForeignKey(Userdetails, on_delete=models.CASCADE)
    Email = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=10)
    Amount = models.DecimalField(max_digits=10, decimal_places=2)

def __str__(self):
        return self.GuestFullName