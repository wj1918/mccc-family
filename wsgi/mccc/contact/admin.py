from django.contrib import admin
from .models import UpdateInvite


class UpdateInviteAdmin(admin.ModelAdmin):
    list_display = ('id','update_family', 'access_token','invite_state','invite_person','invite_email','expiration_date', 'address','home_phone','worship','last_nm1','first_nm1', 'chinese_nm1', 'cell_phone1', 'first_nm2', 'chinese_nm2', 'cell_phone2','creation_date',)
    list_filter = ['invite_state','worship',]
    search_fields = ('access_token','address','home_phone','last_nm1','invite_email','first_nm1', 'chinese_nm1', 'cell_phone1', 'first_nm2', 'chinese_nm2', 'cell_phone2',)
    ordering = ['last_nm1']

admin.site.register(UpdateInvite,UpdateInviteAdmin)
