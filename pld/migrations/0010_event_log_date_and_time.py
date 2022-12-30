# Generated by Django 4.1.1 on 2022-10-10 06:19

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("pld", "0009_event_log"),
    ]

    operations = [
        migrations.AddField(
            model_name="event_log",
            name="Date_and_time",
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
