# Generated by Django 2.2.24 on 2022-12-04 23:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pld', '0015_auto_20221205_0512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event_registration',
            name='Event_startDate',
            field=models.DateField(),
        ),
    ]
