from django.db import models
from family.models import Person
from family.models import Family
from member.models import McccDir
from django.contrib.auth.models import (User, Group,)

class DirUpdate(models.Model):
    
    ACTIVE = 'A'
    CANCELLED = 'C'
    EXPIRED = 'E'
    SENT ='L'
    SUBMITTED ='S'
    FAILED ='F'
    INVITE_STATE = (
        (ACTIVE, 'Active'),
        (CANCELLED, 'Cancelled'),
        (EXPIRED, 'Expired'),
        (SENT, 'Sent'),
        (SUBMITTED, 'Submitted'),
        (FAILED, 'Failed'),
    )
    
    COUPLE='C'
    SINGLE='S'
    DIR_TYPE = (
        (COUPLE, 'Couple'),
        (SINGLE, 'Single'),
    )
                                      
    access_token = models.CharField( max_length=40)
    family = models.ForeignKey( Family, verbose_name="family") 
    full_address = models.CharField( max_length=130, blank=True, null=True)
    home_phone = models.CharField( max_length=40, blank=True, null=True) 
    worship = models.CharField( max_length=9, blank=True, null=True)
    dir_type  = models.CharField( max_length=1, choices=DIR_TYPE, default=COUPLE, verbose_name="type")
    invite_state  = models.CharField( max_length=1, choices=INVITE_STATE, default=ACTIVE)
    invite_email = models.CharField( max_length=200, null=True)
    address = models.CharField( max_length=100, null=True)
    city = models.CharField( max_length=100, null=True)
    state = models.CharField( max_length=100, null=True)
    zip = models.CharField( max_length=100, null=True)

    person1 = models.ForeignKey( Person, null=True, related_name="person1")
    login_user_nm1 = models.ForeignKey( User, blank=True, null=True, related_name="invite1s")
    last_nm1 = models.CharField(max_length=30, blank=True, null=True, verbose_name="Last_NM")
    first_nm1 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM1_E")
    chinese_nm1 = models.CharField( max_length=20, blank=True, null=True, verbose_name="NM1_C")
    cell_phone1 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM1_Cell")
    email1 = models.CharField( max_length=100, null=True,blank=True,)
    fellowship_nm1 = models.CharField( max_length=50, blank=True, null=True,)

    person2 = models.ForeignKey( Person, null=True,blank=True, related_name="person2")
    login_user_nm2 = models.ForeignKey( User, blank=True, null=True, related_name="invite2s")
    first_nm2 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM2_E")
    chinese_nm2 = models.CharField( max_length=20, blank=True, null=True, verbose_name="NM2_C")
    cell_phone2 = models.CharField( max_length=40, blank=True, null=True, verbose_name="NM2_Cell")
    email2 = models.CharField( max_length=100, null=True,blank=True,)
    fellowship_nm2 = models.CharField( max_length=50, blank=True, null=True,)
    
    creation_date = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True,null=True)
    expiration_date = models.DateTimeField(null=True)

    comment =  models.TextField(null=True,blank=True,)

    def __unicode__(self):    
        return self.invite_email
    
    class Meta:
        db_table = 'MCCC_Dir_Update'
        verbose_name_plural = 'Directory Updates'
        verbose_name ='Directory Update'
