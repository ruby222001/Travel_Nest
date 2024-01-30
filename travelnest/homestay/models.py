from django.db import models
class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('khalti', 'Khalti'),
        ('arrival', 'Pay on Arrival'),
    ]

    GuestFullName = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    PhoneNumber = models.CharField(max_length=10)
    paymentmethod = models.CharField(max_length=100, choices=PAYMENT_METHOD_CHOICES, default='khalti')

    def __str__(self):
        return f"{self.GuestFullName} - {self.paymentmethod}"