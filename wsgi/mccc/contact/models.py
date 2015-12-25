from django.db import models
from family.models import Person
from family.models import Family
from member.models import McccDir

class UpdateInvite(models.Model):
    
    ACTIVE = 'A'
    CANCELLED = 'C'
    EXPIRED = 'E'
    INVITE_STATE = (
        (ACTIVE, 'Active'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),
    )
                                      
    access_token = models.CharField( max_length=40)
    invite_state  = models.CharField( max_length=1, choices=INVITE_STATE, default=ACTIVE)
    invite_person = models.ForeignKey( Person, null=True)
    invite_email = models.CharField( max_length=100, null=True)
    update_family = models.ForeignKey( Family, verbose_name="family") 
    address = models.CharField( max_length=130, blank=True, null=True)
    home_phone = models.CharField( max_length=40, blank=True, null=True) 
    worship = models.CharField( max_length=9, blank=True, null=True)

    last_nm1 = models.CharField(max_length=30, blank=True, null=True, verbose_name="Last_NM")
    first_nm1 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM1_E")
    chinese_nm1 = models.CharField( max_length=20, blank=True, null=True, verbose_name="NM1_C")
    cell_phone1 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM1_Cell")

    first_nm2 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM2_E")
    chinese_nm2 = models.CharField( max_length=20, blank=True, null=True, verbose_name="NM2_C")
    cell_phone2 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM2_Cell")
    
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()

    class Meta:
        db_table = 'MCCC_Update_Invite'


