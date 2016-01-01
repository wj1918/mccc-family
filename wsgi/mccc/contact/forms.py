
from django import forms

class ContactForm(forms.Form):
    address=forms.CharField(max_length=200)
    city=forms.CharField(max_length=100)
    state=forms.CharField(max_length=100)
    zip=forms.CharField(max_length=100)
    home_phone=forms.CharField(max_length=100)
    cell_phone1=forms.CharField(max_length=100)
    cell_phone2=forms.CharField(max_length=100)

    