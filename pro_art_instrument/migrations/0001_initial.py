# Generated by Django 2.2.13 on 2022-09-21 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='instrument_details',
            fields=[
                ('instrument_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('instrument_name', models.CharField(max_length=200)),
                ('instrument_amount', models.IntegerField()),
                ('allow_in_public', models.BooleanField(default=0)),
            ],
        ),
    ]
