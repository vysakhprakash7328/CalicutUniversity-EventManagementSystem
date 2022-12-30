from django.contrib import admin
from pro_art_instrument.models import instrument_details

from users.models import Main_accounts

from .models import Event_registration, EventCategory, Hall_details, track
from Unions.models import unions

# Register your models here.

# admin.site.register(Hall_details)

# admin.site.register(Event_registration)
# Remove Groups


@admin.register(Hall_details)
class HallAdmin(admin.ModelAdmin):
    list_display = ('Hall_name','Hall_location','Hall_availability')
    ordering = ('Hall_name','Hall_id')
    search_fields = ('Hall_name','Hall_id')




@admin.register(Event_registration)


class EventAdmin(admin.ModelAdmin):
    list_display = ('Event_name','Event_venue','Event_startDate','Event_endDate')
    ordering = ('Event_name','Event_id')
    list_filter = ('Event_startDate','Event_venue')
    search_fields = ('Event_name','Event_startDate')

@admin.register(EventCategory)
class CatAdmin(admin.ModelAdmin):
    list_display = ('Category_name',)


@admin.register(instrument_details)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('instrument_name',)





admin.site.register(Main_accounts)
admin.site.register(unions)
admin.site.register(track)





















