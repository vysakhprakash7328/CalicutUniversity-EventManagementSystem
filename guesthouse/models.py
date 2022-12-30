from django.db import models



# Create your models here.
class guesthouse_rooms(models.Model):
    room_id = models.IntegerField(primary_key=True)
    room_type = models.CharField(max_length=200)
    room_desc = models.CharField(max_length=400)
    room_rent = models.IntegerField()
    room_img = models.ImageField(null=True, blank=True,upload_to="guest_house/")
    room_available = models.IntegerField() 
    def __str__(self):
        return self.room_type





class bookingDetails(models.Model):
    booking_id=models.IntegerField(primary_key=True)
    room_type=models.CharField(max_length=200)
    number_of_rooms=models.IntegerField()
    check_in=models.DateField(null=True,blank=True)
    check_out=models.DateField(null=True,blank=True)
    person_name=models.CharField(max_length=200)
    room_rate=models.IntegerField()
    status=models.IntegerField()
    number_of_persons=models.IntegerField()
    name =models.CharField(max_length=100)
