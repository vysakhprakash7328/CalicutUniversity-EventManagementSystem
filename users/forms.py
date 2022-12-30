

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms import ModelForm
from users.models import DepartmentHead
from .models import Department, Main_accounts



class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	# department_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'
		
		




class DepartmentHeadRegistration(ModelForm):
	department_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	head_mail = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	head_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))

	# department_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

	
	class Meta:
		model = DepartmentHead 
		fields = ('department_name','head_mail','head_name')

	def __init__(self, *args, **kwargs):
		super(DepartmentHeadRegistration, self).__init__(*args, **kwargs)

		self.fields['department_name'].widget.attrs['class'] = 'form-control'
		self.fields['head_mail'].widget.attrs['class'] = 'form-control'
		self.fields['head_name'].widget.attrs['class'] = 'form-control'





class RegisterDepartmentForm(ModelForm):
    
	department_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	department_password = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	department_name = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))

    
	class Meta:
		model = Department
		fields = ( 'department_email', 'department_password', 'department_name')



	def __init__(self, *args, **kwargs):
		super(RegisterDepartmentForm, self).__init__(*args, **kwargs)

		self.fields['department_email'].widget.attrs['class'] = 'form-control'
		self.fields['department_password'].widget.attrs['class'] = 'form-control'
		self.fields['department_name'].widget.attrs['class'] = 'form-control'
		
		



# Create a varification user form

class AdduserForm(ModelForm):
	name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	password =forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	type = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	varification_choices = forms.Select() #select values are verification and nonverification 
	
	
		
	

    
	class Meta:
		model = Main_accounts

	
		fields = ('name','email','username', 'password', 'type','varification_choices')
		widgets = {
			'varification_choices': forms.Select(attrs={'class':'form-control', 'placeholder':'Hall specification'}),
		}





	
		
	
		