# Generated by Django 4.1.1 on 2022-10-04 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("public", "0004_public_registration_status"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="public_registration",
            name="public_username",
        ),
    ]