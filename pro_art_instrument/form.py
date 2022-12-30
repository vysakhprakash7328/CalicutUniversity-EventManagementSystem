
from django import forms
from django.forms import ModelForm

from pld.models import Event_registration
from .models import instrument_details

class addinstrumentform(ModelForm):
	class Meta:
		model = instrument_details
		fields =('instrument_name','instrument_amount','allow_in_public')
        

		labels = {
			'instrument_name': 'Instrument Name',
            'instrument_amount': 'Instrument Amount ',
			'allow_in_public': 'Allow in Public',

			
            		
		}
		widgets = {
			'instrument_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instrument Name'}),
            'instrument_amount': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instrument amount'}),
			'allow_in_public': forms.CheckboxInput()
			
		}

class uploadimageform(forms.ModelForm):
    class Meta:
        model = Event_registration
        fields = ('Image_description','Event_images', )
