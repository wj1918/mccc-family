from django.db import models
from family.models import Person
from family.models import Family
from member.models import McccDir

class UpdateInvite(models.Model):
    
    ACTIVE = 'A'
    CANCELLED = 'C'
    EXPIRED = 'E'
    LOGIN_EXISTS ='L'
    INVITE_STATE = (
        (ACTIVE, 'Active'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),
        (LOGIN_EXISTS, 'Login Existss'),
    )
    
    COUPLE='C'
    SINGLE='S'
    DIR_TYPE = (
        (COUPLE, 'Couple'),
        (SINGLE, 'Single'),
    )
                                      
    access_token = models.CharField( max_length=40)
    update_family = models.ForeignKey( Family, verbose_name="family") 
    address = models.CharField( max_length=130, blank=True, null=True)
    home_phone = models.CharField( max_length=40, blank=True, null=True) 
    worship = models.CharField( max_length=9, blank=True, null=True)
    dir_type  = models.CharField( max_length=1, choices=DIR_TYPE, default=COUPLE, verbose_name="type")
    invite_email = models.CharField( max_length=200, null=True)

    person1 = models.ForeignKey( Person, null=True, related_name="person1")
    invite_state1  = models.CharField( max_length=1, choices=INVITE_STATE, default=ACTIVE)
    last_nm1 = models.CharField(max_length=30, blank=True, null=True, verbose_name="Last_NM")
    first_nm1 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM1_E")
    chinese_nm1 = models.CharField( max_length=20, blank=True, null=True, verbose_name="NM1_C")
    cell_phone1 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM1_Cell")
    email1 = models.CharField( max_length=100, null=True)

    person2 = models.ForeignKey( Person, null=True, related_name="person2")
    invite_state2  = models.CharField( max_length=1, choices=INVITE_STATE, default=ACTIVE)
    first_nm2 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM2_E")
    chinese_nm2 = models.CharField( max_length=20, blank=True, null=True, verbose_name="NM2_C")
    cell_phone2 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM2_Cell")
    email2 = models.CharField( max_length=100, null=True)
    
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,null=True)
    expiration_date = models.DateTimeField(null=True)

    comment = models.CharField( max_length=400, null=True)
    
    class Meta:
        db_table = 'MCCC_Update_Invite'


