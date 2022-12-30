from django.db import models

# Create your models here.
class instrument_details(models.Model):

    instrument_name = models.CharField(max_length=200)
    instrument_amount = models.IntegerField()
    allow_in_public = models.BooleanField(default=0)