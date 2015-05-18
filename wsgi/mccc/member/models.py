from django.db import models

class McccDir(models.Model):
    family_id = models.IntegerField(db_column='FamilyID',primary_key=True)  # Field name made lowercase.
    last_nm = models.CharField(db_column='Last_NM', max_length=30, blank=True, primary_key=True)  # Field name made lowercase.
    first_nm = models.CharField(db_column='First_NM', max_length=40, blank=True)  # Field name made lowercase.
    chinese_nm = models.CharField(db_column='Chinese_NM', max_length=20, blank=True)  # Field name made lowercase.
    wf_first = models.CharField(db_column='WF_First', max_length=40, blank=True)  # Field name made lowercase.
    wf_chinese_nm = models.CharField(db_column='WF_Chinese_NM', max_length=20, blank=True)  # Field name made lowercase.
    home_phone = models.CharField(db_column='Home_Phone', max_length=40, blank=True)  # Field name made lowercase.
    work_phone = models.CharField(db_column='Work_Phone', max_length=83, blank=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=130, blank=True)  # Field name made lowercase.
    worship = models.CharField(db_column='Worship', max_length=9, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MCCC_Dir'
