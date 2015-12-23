
from django import forms

class ContactForm(forms.Form):
    home_address=forms.CharField(max_length=200)
    home_phone=forms.CharField(max_length=100)
    cell_phone1=forms.CharField(max_length=100)
    cell_phone2=forms.CharField(max_length=100)

    