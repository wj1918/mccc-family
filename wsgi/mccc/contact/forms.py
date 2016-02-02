
from django import forms

class ContactForm(forms.Form):
    YES_NO_CHOICES=[('Y','Yes'),
         ('N','No')]
         
    address=forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Address'}), required=True)
    city=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'City'}), required=True)
    state=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'State'}), required=True)
    zip=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Zip'}), required=True)
    home_phone=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Home Phone'}), required=True)
    chinese_nm1=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell_phone1=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    chinese_nm2=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    cell_phone2=forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class': 'form-control'}))
    mccc_dir=forms.ChoiceField(choices=YES_NO_CHOICES, widget=forms.RadioSelect(), required=True)
