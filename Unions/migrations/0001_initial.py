# Generated by Django 2.2.13 on 2022-08-09 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='unions',
            fields=[
                ('union_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('union_name', models.CharField(max_length=200)),
                ('union_email', models.EmailField(max_length=254, unique=True)),
                ('president_name', models.CharField(max_length=200)),
                ('president_phone', models.IntegerField()),
                ('Secretary_name', models.CharField(max_length=200)),
                ('secretary_phone', models.IntegerField()),
                ('union_username', models.CharField(max_length=200, unique=True)),
                ('union_password', models.CharField(max_length=200)),
            ],
        ),
    ]
