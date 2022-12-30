from django.contrib import admin

from guesthouse.models import guesthouse_rooms,bookingDetails

# Register your models here.

admin.site.register(guesthouse_rooms)
admin.site.register(bookingDetails)