from django.contrib import admin
from .models import UpdateInvite
from .utils import send_email
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .utils import create_logins
from django.contrib.admin import helpers
from profile.models import UserProfile
from django.db.models import Q

class UpdateInviteAdmin(admin.ModelAdmin):
    list_display = ('id','dir_type','invite_email','get_has_login','invite_state', 'access_token','expiration_date','full_address', 'address','city','state','zip','home_phone','worship','person1','last_nm1','first_nm1', 'chinese_nm1', 'cell_phone1','email1','fellowship_nm1','person2', 'first_nm2', 'chinese_nm2', 'cell_phone2','email2','fellowship_nm2','creation_date',)
    list_filter = ['worship','dir_type','invite_state','fellowship_nm1',]
    search_fields = ('access_token','address','home_phone','last_nm1','first_nm1', 'chinese_nm1', 'cell_phone1','email1', 'first_nm2', 'chinese_nm2', 'cell_phone2','email2',)
    ordering = ['last_nm1']

    def get_has_login(self, obj):
        if obj.person1 and UserProfile.objects.filter(person__id=obj.person1.id).exists():
            return True
        if obj.person2 and UserProfile.objects.filter(person__id=obj.person2.id).exists():
            return True
        return False
        
    get_has_login.short_description = 'Has Login'

    def send_invite_email(self, request, queryset):
        idvallist=queryset.values_list('id', flat=True)
        first_id=idvallist.first()
        ids_str=",".join( str( val ) for val in idvallist )
        request.session["ids"]=ids_str
        request.session["first_id"]=first_id
        return HttpResponseRedirect(reverse("contact:preview"))
    send_invite_email.short_description = "Send Welcome Emails"


    def create_logins(self, request, queryset):
        if request.POST.get('post'):
            # process the queryset here
            rows_updated = create_logins(queryset)
            if rows_updated == 1:
                message_bit = "1 login user was"
            else:
                message_bit = "%s login users were" % rows_updated
            self.message_user(request, "%s successfully created." % message_bit)
        else:
            context = {
                'title': "Are you sure?",
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,                
            }
            return TemplateResponse(request, 'contact/create_login_preview.html',context)
#            return TemplateResponse(request, "admin/delete_selected_confirmation.html" ,context)
          
    create_logins.short_description = "Create Logins"

    actions = [send_invite_email,create_logins,]
    
admin.site.register(UpdateInvite,UpdateInviteAdmin)
