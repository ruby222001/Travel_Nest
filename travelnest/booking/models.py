from django.db import models
from homestay.models import HomeStay
from django.conf import settings

# Create your models here.


class Booking(models.Model):
    PAYMENT_CHOICES = [
        ('Khalti', 'Khalti'),
        ('Pay on Arrival', 'Pay on Arrival'),
    ]

    homestay = models.ForeignKey(HomeStay, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    num_guests = models.IntegerField()
    amount = models.IntegerField()
    payment_type = models.CharField(max_length=20, choices=PAYMENT_CHOICES)


class Review(models.Model):
    homestay = models.ForeignKey(HomeStay, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating} stars"
