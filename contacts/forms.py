from django import forms
from .models import ContactInfo

class ContactInfoForm(forms.ModelForm):

	class Meta:
		model = ContactInfo
		fields = {'first_name','last_name','contact_number','address',}