# Generated by Django 2.2.13 on 2022-09-23 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pld', '0005_event_registration_art_permission'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_registration',
            name='Event_images',
            field=models.ImageField(blank=True, null=True, upload_to='eventimage/'),
        ),
    ]