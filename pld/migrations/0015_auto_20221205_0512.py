# Generated by Django 2.2.24 on 2022-12-04 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pld', '0014_auto_20221017_0545'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_registration',
            name='Event_startDate',
            field=models.DateTimeField(),
        ),
    ]
