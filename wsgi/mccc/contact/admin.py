from django.contrib import admin
from .models import UpdateInvite
from .utils import send_email
from django.template.response import TemplateResponse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

class UpdateInviteAdmin(admin.ModelAdmin):
    list_display = ('id','update_family','invite_state','invite_person','is_member','invite_email',"dir_type", 'access_token','expiration_date', 'address','home_phone','worship','last_nm1','first_nm1', 'chinese_nm1', 'cell_phone1', 'first_nm2', 'chinese_nm2', 'cell_phone2','creation_date','comment',)
    list_filter = ['invite_state','worship','dir_type','is_member',]
    search_fields = ('access_token','address','home_phone','last_nm1','invite_email','first_nm1', 'chinese_nm1', 'cell_phone1', 'first_nm2', 'chinese_nm2', 'cell_phone2',)
    ordering = ['last_nm1']

    def send_invite_email(self, request, queryset):
        vallist=queryset.values_list('id', flat=True)
        first_id=vallist.first()
        ids=",".join( str( val ) for val in vallist )
        request.session["ids"]=ids
        request.session["first_id"]=first_id
        #return TemplateResponse(request, 'contact/preview.html', {"ids":ids})
        return HttpResponseRedirect(reverse("contact:preview"))
        # return HttpResponseRedirect("/contact/preview/")
    
    send_invite_email.short_description = "Send invite email"

    actions = [send_invite_email,]
    
admin.site.register(UpdateInvite,UpdateInviteAdmin)
