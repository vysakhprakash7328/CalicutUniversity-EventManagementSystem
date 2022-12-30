from django.forms import ModelForm
from django import forms

from Unions.models import unions




class UnionRegistrationForm(ModelForm):
	union_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	union_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	president_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	president_phone = forms.IntegerField()
	secretary_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class':'form-control'}))
	secretary_phone = forms.IntegerField()


	
	class Meta:
		model =  unions
		fields = ('union_name','union_email','president_name','president_phone','secretary_name','secretary_phone',)

	def __init__(self, *args, **kwargs):
		super(UnionRegistrationForm, self).__init__(*args, **kwargs)

		self.fields['union_name'].widget.attrs['class'] = 'form-control'
		self.fields['union_email'].widget.attrs['class'] = 'form-control'
		self.fields['president_name'].widget.attrs['class'] = 'form-control'
		self.fields['president_phone'].widget.attrs['class'] = 'form-control'
		self.fields['secretary_name'].widget.attrs['class'] = 'form-control'
		self.fields['secretary_phone'].widget.attrs['class'] = 'form-control'

