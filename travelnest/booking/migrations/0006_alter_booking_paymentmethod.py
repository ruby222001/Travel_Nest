# Generated by Django 4.1.7 on 2023-12-25 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0005_remove_booking_paymentmethod_booking_paymentmethod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='paymentMethod',
            field=models.CharField(choices=[('khalti', 'Khalti'), ('arrival', 'Pay on Arrival')], max_length=255),
        ),
    ]