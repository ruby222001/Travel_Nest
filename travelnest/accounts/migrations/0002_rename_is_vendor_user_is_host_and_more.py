# Generated by Django 4.2.1 on 2023-10-23 09:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_vendor',
            new_name='is_host',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_customer',
            new_name='is_user',
        ),
        migrations.DeleteModel(
            name='Payment',
        ),
    ]