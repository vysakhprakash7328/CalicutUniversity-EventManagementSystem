# Generated by Django 4.1.1 on 2022-10-11 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pld", "0011_alter_event_log_event_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event_log",
            name="Event_id",
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]