# Generated by Django 4.1.1 on 2022-10-11 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pld", "0010_event_log_date_and_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event_log",
            name="Event_id",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
