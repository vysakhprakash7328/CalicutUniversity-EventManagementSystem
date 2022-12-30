# Generated by Django 2.2.13 on 2022-09-21 07:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pro_art_instrument', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='instrument_details',
            name='instrument_id',
        ),
        migrations.AddField(
            model_name='instrument_details',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]