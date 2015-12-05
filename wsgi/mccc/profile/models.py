# models.py
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class ProfileFamily(models.Model):
    def __unicode__(self):
        list0 = [self.address, self.city, self.state, self.zip]
        faddress =[x for x in list0 if x is not None]
        return u','.join(faddress).encode('utf-8').strip()
    id = models.AutoField(db_column='FamilyID',primary_key=True,verbose_name="Family ID")
    status = models.CharField(db_column='Status', max_length=2, blank=True, help_text="A -- Active, I -- Inactive, L -- Local Inactive, O -- Out of Date, N -- New, R -- Remote")  # Field name made lowercase.
    home1 = models.CharField('Home Phone', db_column='Home1', max_length=40, blank=True)  # Field name made lowercase.
    homefax = models.CharField('Home Fax', db_column='HomeFax', max_length=40, blank=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=40, blank=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=4, blank=True)  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=20, blank=True)  # Field name made lowercase.
    class Meta:
        db_table = 'MCCC_Family'
        managed = False
        verbose_name_plural = 'Families'
        verbose_name ='Family'


class ProfilePerson(models.Model):
    def __unicode__(self):    
        list0 = [self.first, self.last]
        flist =[x for x in list0 if x is not None]
        firstlast= u','.join(flist).encode('utf-8').strip()
        return u' '.join((firstlast, self.chinese)) if self.chinese else firstlast
    id = models.AutoField(db_column='PersonID',primary_key=True,verbose_name="Person ID")
    last = models.CharField(db_column='Last', max_length=30, blank=True)  # Field name made lowercase.
    first = models.CharField(db_column='First', max_length=40, blank=True)  # Field name made lowercase.
    middle = models.CharField(db_column='Middle', max_length=20, blank=True)  # Field name made lowercase.
    chinese = models.CharField(db_column='Chinese', max_length=20, blank=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=2, blank=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=4, blank=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True)  # Field name made lowercase.
    cphone = models.CharField('Cell Phone', db_column='CPhone', max_length=510, blank=True)  # Field name made lowercase.
    birthday = models.DateField('Brithday', db_column='Birthday', blank=True, null=True)  # Field name made lowercase.
    family = models.ForeignKey(ProfileFamily,db_column='FamilyID',related_name="persons")
    class Meta:
        db_table = 'MCCC_Person'
        managed = False
        verbose_name_plural = 'Persons'
        verbose_name = 'Person'

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    person =models.OneToOneField(ProfilePerson)
    def __unicode__(self):
        return self.user.username
    class Meta:
        db_table = 'user_profile'
