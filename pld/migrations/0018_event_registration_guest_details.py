# Generated by Django 2.2.24 on 2022-12-08 00:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pld', '0017_event_registration_event_starttime'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_registration',
            name='Guest_details',
            field=models.CharField(default=django.utils.timezone.now, max_length=250),
            preserve_default=False,
        ),
    ]
