
from distutils.command.upload import upload
from pyexpat import model
from random import choices

from django.db import models
from django.contrib.auth.models import User
from pro_art_instrument.models import instrument_details

from users.models import Main_accounts

# Create your models here.



my_choicesforspec=[
    ('AC','A/C'),('Non A/C','Non A/C')
]

class Hall_details(models.Model):
    Hall_id=models.CharField(primary_key=True,max_length=200)
    Hall_name=models.CharField(max_length=200)
    Hall_capacity=models.IntegerField()
    Hall_location=models.CharField(max_length=200)
    Hall_availability=models.BooleanField(default=False)
    Hall_spesification=models.CharField(max_length=20, choices = my_choicesforspec,default=my_choicesforspec[0])
    Hall_manager = models.CharField(max_length=100)
    public_view = models.BooleanField(default=False)
    Amount = models.IntegerField(null=True,blank=True)
    Due_date = models.DateField(null=True,blank=True)
    NewAmount = models.IntegerField(null=True,blank=True)
    Hall_images = models.ImageField(null=True,blank=True,upload_to = 'hallimage/')

    
    def __str__(self):
        return self.Hall_name



class EventCategory(models.Model):
    Category_id = models.IntegerField(primary_key=True)
    Category_name = models.CharField(max_length=200)

    def __str__(self):
        return self.Category_name


class Event_registration(models.Model):
    Event_id=models.BigAutoField(primary_key=True)
    Event_name=models.CharField(max_length=200)
    Event_venue=models.ForeignKey(Hall_details, on_delete=models.CASCADE)
    Category_name=models.IntegerField(blank=True,null=True)
    Event_startDate=models.DateField()
    Event_startTime = models.TimeField(null=True,blank=True)
    Event_endDate=models.DateField()
    Event_description=models.CharField(max_length=200,blank=True)
    Event_status=models.IntegerField(default=0)
    Event_manager = models.CharField(max_length=200)
    Guest_details = models.CharField(max_length=250)
    Instrument_details = models.CharField(max_length=200,null=True,blank=True)
    public = models.BooleanField(default=False)
    Art_and_Photography = models.BooleanField(default=False)
    Resubmission = models.IntegerField(default=0)
    art_permission = models.IntegerField(default=0)
    waiting_list = models.IntegerField(default=0)
    Event_amount = models.IntegerField(null=True,blank=True)
    Event_images = models.ImageField(null=True,blank=True,upload_to = 'Eventimage/')
    Image_description = models.CharField(max_length=200,blank=True,null=True)



    def __str__(self):
        return self.Event_name



    


class track(models.Model):
    event_id = models.IntegerField()
    approved_by = models.CharField(max_length=200)
    approved_on = models.DateTimeField(null=True,blank=True)
    remarks = models.CharField(max_length=200,null=True,blank=True)
    status= models.IntegerField(default=0)

    def __str__(self):
        return self.approved_by

class payment_details(models.Model):
    Event_id = models.IntegerField()
    Challan_number = models.CharField(max_length=200)
    Payment_datetime = models.DateTimeField()
    Amount = models.IntegerField()
    Treasury = models.CharField(max_length=200)
    Payer_name = models.CharField(max_length=200)

class Event_log(models.Model):
    log_id = models.BigAutoField(primary_key = True)
    operation = models.CharField(max_length=200)
    person_name = models.CharField(max_length = 200)
    person_category = models.CharField(max_length = 200)
    Event_id = models.CharField(max_length = 200,blank = True,null = True)
    Date_and_time = models.DateTimeField()
