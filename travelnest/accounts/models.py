from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    is_host = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)
    image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    mobile=models.CharField(max_length=20,null=True,blank=True)
    address=models.TextField(null=True, blank=True)