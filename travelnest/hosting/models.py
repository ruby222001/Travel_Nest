from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from accounts.models import User

# Create your models here.


class Homestay(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
    homestay_name = models.CharField(max_length=255)
    address = models.TextField()
    location = models.CharField(max_length=255)
    thumbnail_picture = models.ImageField(upload_to='homestay_thumbnails/')
    # secondary_pictures = models.ManyToManyField(ImageGallery, related_name='homestay_secondary_pictures', blank=True)
    citizenship_photo = models.ImageField(upload_to='citizenship_photos/')
    email = models.EmailField()
    mobile_number = models.CharField(max_length=20)
    ownership_document_photo = models.ImageField(upload_to='ownership_document_photos/')
    features = models.TextField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='approved')
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_homestays', blank=True)
    price=models.CharField(max_length=25,default=2500)

    def __str__(self):
        return self.homestay_name
    

# class Liked(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     liked = models.ForeignKey(Homestay, on_delete=models.CASCADE)