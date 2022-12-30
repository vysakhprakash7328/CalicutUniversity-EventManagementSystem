from email.policy import default
from django.db import models

# Create your models here.
class public_registration(models.Model):
    public_name = models.CharField(max_length=200)
    public_email = models.EmailField()
    public_phone = models.IntegerField()
    public_address = models.CharField(max_length=200)
    public_location = models.CharField(max_length=200)
    public_password = models.CharField(max_length=200)
    status = models.IntegerField(default=0)