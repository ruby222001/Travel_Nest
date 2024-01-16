from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from hosting.models import HomeStay

# Create your models here.


class Booking(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('khalti', 'Khalti'),
        ('arrival', 'Pay on Arrival'),
    ]
    homestay = models.ForeignKey(HomeStay, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.IntegerField()
    price_per_night=models.IntegerField()
    
    paymentMethod = models.CharField(max_length=255, choices=PAYMENT_METHOD_CHOICES, ) 
    @property
    def price_per_night(self):
        return self.homestay.price_per_night
    @property
    def total_price_per_night(self):
        return self.price_per_night * (self.check_out_date - self.check_in_date).days
    def __str__(self):
        return f"{self.user.username} - {self.paymentMethod}"

class Review(models.Model):
    homestay = models.ForeignKey(HomeStay, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"
    



