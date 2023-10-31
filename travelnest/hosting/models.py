from django.db import models

# Create your models here.


class Homestay(models.Model):
    name = models.CharField(max_length=255)
    photo = models.ImageField(upload_to='homestay_photos/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    location = models.CharField(max_length=255)
    features = models.TextField()
    
    def __str__(self):
        return self.name