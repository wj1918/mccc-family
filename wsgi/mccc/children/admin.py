from django.contrib import admin
from django.contrib.admin import AdminSite
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from children.models import CmMaster
from family.models import Person
import autocomplete_light

class ChildrenSite(AdminSite):
    site_header = 'Children'
    
    def login(self, request, extra_context=None):
        return redirect('home')

class CmMasterAdmin(admin.ModelAdmin):
    list_display = ['first_last','first_last','ssgrade','ssactive','choiractive','choirgrade','fname','lname','chinese_name','gender','grade','dob',
    'allergies_medical_conditions_medications','fathers_english_name','fathers_chinese_name_if_available','mothers_english_name','mother_chinese_name_if_available',
    'email','street','city','state','zip','home','fathers_office','fathers_cell','mothers_office','mothers_cell','alternate_contact_name','alt_contact_main_phone',
    'altcont','mccc','group','assign','christianfather','christianmother','remarks','felly']
    search_fields = ['first_last','fname','lname','chinese_name','allergies_medical_conditions_medications','fathers_english_name','fathers_chinese_name_if_available','mothers_english_name','mother_chinese_name_if_available',
    'email','street','city','state','zip','home']
    list_filter = ['ssactive','ssgrade','choiractive','choirgrade']
    form = autocomplete_light.modelform_factory(CmMaster,exclude=[])
    
# for the person raw_id picker widget 
# The raw_id_fields widget shows a magnifying glass button next to the field which allows users to search for and select a value
class PersonPicker(admin.ModelAdmin):
    list_display = ('id','last','first','chinese','sex','email', 'cphone','role','birthday',)
    search_fields = ['last','first','chinese','email', 'cphone',]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

children_site = ChildrenSite(name='children')
        
children_site.register(CmMaster,CmMasterAdmin)
children_site.register(Person, PersonPicker)
