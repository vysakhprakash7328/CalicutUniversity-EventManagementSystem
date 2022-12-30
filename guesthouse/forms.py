from django import forms
from django.forms import ModelForm

from.models import guesthouse_rooms



class roomdetailsform(ModelForm):
	# Event_startDate = forms.DateField(validators=[present_or_future_date],widget = forms.SelectDateWidget())
	class Meta:
		model = guesthouse_rooms
		fields =('room_type','room_desc','room_rent','room_available','room_img')
        

		labels = {
			'room_type': 'Room type',
            'room_desc': 'Room description',
			'room_rent': 'Room rent ',
            'room_available':'Room available',
			'room_img':'upload a image'

			
        
            		
		}
		widgets = {
			'room_type': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Type'}),
            'room_desc': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Room description'}),
			'room_rent': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room rent'}),
			'room_available': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Available Rooms'}),
		

			
		}


class roombookingForm(ModelForm):
	# Event_startDate = forms.DateField(validators=[present_or_future_date],widget = forms.SelectDateWidget())
	class Meta:
		model = guesthouse_rooms
		fields =('room_type','room_desc','room_rent','room_available','room_img')
        

		labels = {
			'room_type': 'Room type',
            'room_desc': 'Room description',
			'room_rent': 'Room rent ',
            'room_available':'Room available',
			'room_img':'upload a image'

			
        
            		
		}
		widgets = {
			'room_type': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room Type'}),
            'room_desc': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Room description'}),
			'room_rent': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Room rent'}),
			'room_available': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Available Rooms'}),
		

			
		}
