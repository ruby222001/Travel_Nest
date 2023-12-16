from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Feature(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class HomeStay(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('unapproved', 'Unapproved'),
    ]

    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    num_guests = models.IntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    ownership_documents = models.FileField(upload_to='documents/')
    citizenship_documents = models.FileField(upload_to='documents/')
    thumbnail_image = models.ImageField(upload_to='thumbnails/')
    secondary_images = models.ImageField(upload_to='secondary_images/', blank=True, null=True)
    description = models.TextField()
    features = models.ManyToManyField(Feature)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    liked_by_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_homestays', blank=True)

    def get_like_count(self):
        return self.liked_by_users.count()

    def __str__(self):
        return self.name
    
class HomeStayImage(models.Model):
    homestay = models.ForeignKey(HomeStay, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='secondary_images/')
