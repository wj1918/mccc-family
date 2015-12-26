from django.contrib import admin
from .models import UpdateInvite
from .utils import send_email


class UpdateInviteAdmin(admin.ModelAdmin):
    list_display = ('id','update_family','invite_state','invite_person','is_member','invite_email',"dir_type", 'access_token','expiration_date', 'address','home_phone','worship','last_nm1','first_nm1', 'chinese_nm1', 'cell_phone1', 'first_nm2', 'chinese_nm2', 'cell_phone2','creation_date','comment',)
    list_filter = ['invite_state','worship','dir_type','is_member',]
    search_fields = ('access_token','address','home_phone','last_nm1','invite_email','first_nm1', 'chinese_nm1', 'cell_phone1', 'first_nm2', 'chinese_nm2', 'cell_phone2',)
    ordering = ['last_nm1']
    
    def send_invite_email(self, request, queryset):
        rows_updated = send_email(queryset)
        if rows_updated == 1:
            message_bit = "1 invite email was"
        else:
            message_bit = "%s invite emails were" % rows_updated
        self.message_user(request, "%s successfully sent." % message_bit)
    send_invite_email.short_description = "Send invite email"

    actions = [send_invite_email,]
    

admin.site.register(UpdateInvite,UpdateInviteAdmin)
