# Generated by Django 2.2.24 on 2022-08-08 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20220808_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departmenthead',
            name='status',
            field=models.IntegerField(default=0),
        ),
    ]
