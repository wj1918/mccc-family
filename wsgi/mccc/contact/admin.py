from django.contrib import admin
from .models import UpdateInvite
from .utils import send_email
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class UpdateInviteAdmin(admin.ModelAdmin):
    list_display = ('id','dir_type','invite_email','invite_state', 'access_token','expiration_date','full_address', 'address','city','state','zip','home_phone','worship','person1','last_nm1','first_nm1', 'chinese_nm1', 'cell_phone1','email1','fellowship_nm1','person2', 'first_nm2', 'chinese_nm2', 'cell_phone2','email2','fellowship_nm2','creation_date',)
    list_filter = ['worship','dir_type','invite_state','fellowship_nm1',]
    search_fields = ('access_token','address','home_phone','last_nm1','first_nm1', 'chinese_nm1', 'cell_phone1','email1', 'first_nm2', 'chinese_nm2', 'cell_phone2','email2',)
    ordering = ['last_nm1']

    def send_invite_email(self, request, queryset):
        idvallist=queryset.values_list('id', flat=True)
        first_id=idvallist.first()
        ids_str=",".join( str( val ) for val in idvallist )
        request.session["ids"]=ids_str
        request.session["first_id"]=first_id
        return HttpResponseRedirect(reverse("contact:preview"))

    send_invite_email.short_description = "Send invite email"

    actions = [send_invite_email,]
    
admin.site.register(UpdateInvite,UpdateInviteAdmin)
