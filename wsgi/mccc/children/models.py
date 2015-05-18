# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models

    
class CmMaster(models.Model):
    def __str__(self):
        return self.first_last
    
    id = models.AutoField(primary_key=True)  # AutoField?
    first_last = models.CharField(max_length=100, blank=True)
    ssgroup = models.CharField(max_length=100, blank=True)
    ssgrade = models.CharField(max_length=100, blank=True)
    ssactive = models.CharField(max_length=100, blank=True)
    choiractive = models.CharField(max_length=100, blank=True)
    choirgrade = models.CharField(max_length=100, blank=True)
    fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=100, blank=True)
    chinese_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=100, blank=True)
    std = models.CharField(max_length=100, blank=True)
    dob = models.CharField(max_length=100, blank=True)
    allergies_medical_conditions_medications = models.CharField(max_length=100, blank=True)
    fathers_english_name = models.CharField(max_length=100, blank=True)
    fathers_chinese_name_if_available = models.CharField(max_length=100, blank=True)
    mothers_english_name = models.CharField(max_length=100, blank=True)
    mother_chinese_name_if_available = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zip = models.CharField(max_length=100, blank=True)
    home = models.CharField(max_length=100, blank=True)
    fathers_office = models.CharField(max_length=100, blank=True)
    fathers_cell = models.CharField(max_length=100, blank=True)
    mothers_office = models.CharField(max_length=100, blank=True)
    mothers_cell = models.CharField(max_length=100, blank=True)
    alternate_contact_name = models.CharField(max_length=100, blank=True)
    alt_contact_main_phone = models.CharField(max_length=100, blank=True)
    altcont = models.CharField(max_length=100, blank=True)
    mccc = models.CharField(max_length=100, blank=True)
    number_2010 = models.CharField(db_column='2010', max_length=100, blank=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2011 = models.CharField(db_column='2011', max_length=100, blank=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2012 = models.CharField(db_column='2012', max_length=100, blank=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2013 = models.CharField(db_column='2013', max_length=100, blank=True)  # Field renamed because it wasn't a valid Python identifier.
    number_2014 = models.CharField(db_column='2014', max_length=100, blank=True)  # Field renamed because it wasn't a valid Python identifier.
    group = models.CharField(max_length=100, blank=True)
    assign = models.CharField(max_length=100, blank=True)
    christianfather = models.CharField(max_length=100, blank=True)
    christianmother = models.CharField(max_length=100, blank=True)
    remarks = models.CharField(max_length=100, blank=True)
    felly = models.CharField(max_length=100, blank=True)
    column_ar = models.CharField(db_column='column_AR', max_length=100, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MCCC_CM_Master'
