# Generated by Django 2.2.24 on 2022-12-11 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guesthouse', '0010_bookingdetails_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookingdetails',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]