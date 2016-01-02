
from django import forms

class ContactForm(forms.Form):
    address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address'}))
    city=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'City'}))
    state=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'State'}))
    zip=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Zip'}))
    home_phone=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Home Phone'}))
    last_nm1=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Last Name'}))
    first_nm1=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'First Name'}))
    chinese_nm1=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Chinese Name'}))
    cell_phone1=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Cell Phone'}))
    first_nm2=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Wife Name'}))
    chinese_nm2=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Wife Chinese Name'}))
    cell_phone2=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Wife Cell Phone'}))
