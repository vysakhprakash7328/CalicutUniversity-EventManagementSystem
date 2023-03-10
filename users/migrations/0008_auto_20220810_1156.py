# Generated by Django 2.2.13 on 2022-08-10 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20220808_1100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='main_accounts',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='main_accounts',
            name='type',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='main_accounts',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
