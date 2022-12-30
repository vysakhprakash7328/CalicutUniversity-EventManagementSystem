


from email.policy import default
from Unions.models import unions
from .models import Event_registration, EventCategory, Hall_details
from users.models import DepartmentHead, Main_accounts

from django import forms
from django.forms import ModelForm




#user venue add form
class VenueForm(ModelForm):
	class Meta:
		model = Hall_details
		fields = ('Hall_id','Hall_name','Hall_capacity','Hall_location','Hall_spesification','Hall_availability','public_view','Amount','Hall_images',)
		labels = {
			'Hall_id': 'Hall Id',
			'Hall_name': 'Hall Name',
			'Hall_capacity': 'Hall Capacity',
			'Hall_location': 'Hall Location',
			'Hall_availability': 'Hall Availability',
			'Hall_spesification': 'Hall Specifications',
			'Amount': 'Hall Amount',
			'public_view': 'Allow in public',
			'Hall_images': 'Hall Images'			
		}
		widgets = {
			'Hall_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hall ID'}),
			'Hall_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hall Name'}),
			'Hall_capacity': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hall Capacity'}),
			'Hall_location': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hall location'}),
			
			'Hall_spesification': forms.Select(attrs={'class':'form-control', 'placeholder':'Hall specification'}),
			'Amount': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Hall Amount'}),
			'Hall_availability': forms.CheckboxInput(),
			'public_view': forms.CheckboxInput()
		}









managers = [("admin","admin"),]
manager = Main_accounts.objects.all()
for i in manager:
	if i.varification_choices == 'Varification':
		a=( str(i.name),str(i.name))
		managers.append(a)
		



# Admin SuperUser Event Form
class EventFormAdmin(ModelForm):

	Event_manager = forms.ChoiceField(choices=managers,required=True,disabled=False,widget=forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}))
	
	class Meta:
		model = Event_registration
		fields =('Event_name','Event_venue','Event_manager','Event_startDate','Event_startTime','Event_endDate','Event_description','Category_name')
        

  

		labels = {
			'Event_name': 'Event Name',
              'Event_startDate': 'Start Date ',
              'Event_startTime': 'Start Time ',
			'Event_endDate': 'End Date ',
			'Event_venue': 'Venue',
			'Event_manager': 'Manager',
			
			'Event_description': 'Event Discription',	
			'Category_name':'Category_name',	

            		
		}


		widgets = {
			'Event_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
    'Event_startDate': forms.DateInput(attrs={'class':'form-control datepicker', 'type':'date'}),
			'Event_endDate': forms.DateInput(attrs={'class':'form-control datepicker1', 'type':'date'}),
			'Event_venue': forms.Select(attrs={'class':'form-select', 'placeholder':' Select Venue','id':'select','value':Hall_details.Hall_id}),

			# 'Event_manager': forms.ChoiceField(attrs={'class':'form-select', 'placeholder':'Manager'}),
			'Event_description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
			'Category_name': forms.Select(attrs={'class':'form-select', 'placeholder':'Category_name','id':'category'}),

          

		}

class EventForm(ModelForm):
	# Event_startDate = forms.DateField(validators=[present_or_future_date],widget = forms.SelectDateWidget())
	class Meta:
		model = Event_registration
		
		fields =('Event_name','Event_venue','Event_startDate','Event_startTime','Event_endDate','Event_description','Guest_details','Art_and_Photography')
        

		labels = {
			'Event_name': 'Event Name',
            'Event_startDate': 'Start Date ',
            'Event_startTime': 'Start Time ',
			'Event_endDate': 'End Date ',

			'Event_venue': 'Venue',
			
			
			'Event_description': 'Description',
			'Guest_details':'Guest details',
			'Art_and_Photography': 'Art and PRO',
        
            		
		}
		widgets = {
			'Event_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
            'Event_startDate': forms.DateInput(attrs={'class':'form-control datepicker', 'type':'date'}),
            'Event_startTime': forms.TimeInput(attrs={'class':'form-control', 'type':'time'}),
			'Event_endDate': forms.DateInput(attrs={'class':'form-control datepicker1', 'type':'date'}),
			'Event_venue': forms.Select(attrs={'class':'form-select', 'placeholder':' Select Venue','id':'select','value':Hall_details.Hall_id}),
			'Event_description': forms.Textarea(attrs={'class':'form-control','placeholder':'Description' }),
			'Art_and_Photography':forms.CheckboxInput(),
			'Guest_details': forms.Textarea(attrs={'class':'form-control','placeholder':'Guest details' }),
        

		}

# public event registration form

# publicvenues= []
# publicvenue = Hall_details.objects.filter(public_view = 1)
# for i in publicvenue:
# 	a=( i.Hall_id,str(i.Hall_name))
# 	publicvenues.append(a)
	



class PublicEventForm(ModelForm):
	# Event_venue = forms.ChoiceField(choices=publicvenues,required=True,disabled=False,widget=forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}))
	
	class Meta:
		model = Event_registration
		fields =('Event_name',
		'Event_venue',
		'Event_startDate',
		'Event_endDate',
		'Event_description',
		)
        

		labels = {
			'Event_name': 'Event Name',
            'Event_startDate': 'Start Date ',
			'Event_endDate': 'End Date ',

			'Event_venue': 'Venue',
			
			
			'Event_description': 'Description',	
        
            		
		}
		widgets = {
			'Event_name': forms.TextInput(attrs={'class':'form-control','id':'eventname', 'placeholder':'Event Name'}),
            'Event_startDate': forms.DateInput(attrs={'class':'form-control datepicker', 'type':'date','placeholder':'Start Date'}),
			'Event_endDate': forms.DateInput(attrs={'class':'form-control datepicker1', 'type':'date','placeholder':'End Date'}),
			'Event_venue': forms.Select(attrs={'class':'form-select ','placeholder':'Select Venue','id':'select'}),
			'Event_description': forms.Textarea(attrs={'class':'form-control','placeholder':'Description' }),
        

		}




#user username and password generation form form user app




class DepartmentRequest(ModelForm):
	head_password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

	# department_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

	
	class Meta:
		model = DepartmentHead 
		fields = ('head_password',)

	def __init__(self, *args, **kwargs):
		super(DepartmentRequest, self).__init__(*args, **kwargs)

		self.fields['head_password'].widget.attrs['class'] = 'form-control'


class UnionRequests(ModelForm):
	union_password = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))


	
	class Meta:
		model = unions 
		fields = ('union_password',)

	def __init__(self, *args, **kwargs):
		super(UnionRequests, self).__init__(*args, **kwargs)

		self.fields['union_password'].widget.attrs['class'] = 'form-control'




# admin category form
class CategoryForm(ModelForm):

  
  class Meta:
    model = EventCategory 
    fields = ('Category_name',)




class High_priority_eventForm(ModelForm):

	Event_manager = forms.ChoiceField(choices=managers,required=True,disabled=False,widget=forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}))

	class Meta:
		model = Event_registration
		fields =('Event_name','Event_venue','Event_manager','Event_startDate','Event_endDate','Category_name','Event_description','Art_and_Photography')
		



		labels = {
			'Event_name': 'Event Name',
			'Event_startDate': 'Start Date ',
			'Event_endDate': 'End Date ',
			'Event_venue': 'Venue Id',
			'Event_manager': 'Manager',
			'Art_and_Photography': 'Art and Photography',
			'Event_description': 'Event Discription',	
			'Category_name':'Category_name',	

					
		}


		widgets = {
			'Event_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
			'Event_startDate': forms.DateInput(attrs={'class':'form-control ', 'type':'date','id':'startd'}),
			'Event_endDate': forms.DateInput(attrs={'class':'form-control ', 'type':'date','id':'endd'}),
			'Event_venue': forms.TextInput(attrs={'class':'form-select', 'placeholder':' Select Venue','id':'venue'}),
			'Art_and_Photography':forms.CheckboxInput(),
			# 'Event_manager': forms.ChoiceField(attrs={'class':'form-select', 'placeholder':'Manager'}),
			'Event_description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
			'Category_name': forms.Select(attrs={'class':'form-select', 'placeholder':'Category_name','id':'category'}),

			

		}