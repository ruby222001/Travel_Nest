from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser

# Create your models here.
class User(AbstractUser):
    mobile=models.CharField(max_length=20,null=True,blank=True)
    address=models.TextField(null=True, blank=True)
    is_user=models.BooleanField(default=False)
    is_host=models.BooleanField(default=False)
    


