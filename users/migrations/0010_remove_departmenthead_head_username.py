# Generated by Django 4.1.1 on 2022-09-30 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0009_remove_main_accounts_position"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="departmenthead",
            name="head_username",
        ),
    ]
