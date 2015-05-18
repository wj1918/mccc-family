from django.db import models

# Create your models here.

class Family(models.Model):
    def __unicode__(self):
        list0 = [self.address, self.city, self.state, self.zip]
        faddress =[x for x in list0 if x is not None]
        return u','.join(faddress).encode('utf-8').strip()

    id = models.AutoField(db_column='FamilyID',primary_key=True,verbose_name="Family ID")
    status = models.CharField(db_column='Status', max_length=2, blank=True, help_text="A -- Active, I -- Inactive, L -- Local Inactive, O -- Out of Date, N -- New, R -- Remote")  # Field name made lowercase.
    home1 = models.CharField(db_column='Home1', max_length=40, blank=True)  # Field name made lowercase.
    home2 = models.CharField(db_column='Home2', max_length=40, blank=True)  # Field name made lowercase.
    homefax = models.CharField(db_column='HomeFax', max_length=40, blank=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=100, blank=True)  # Field name made lowercase.
    city = models.CharField(db_column='City', max_length=40, blank=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=4, blank=True)  # Field name made lowercase.
    zip = models.CharField(db_column='Zip', max_length=20, blank=True)  # Field name made lowercase.
      
    class Meta:
        managed = False
        db_table = 'MCCC_Family'

class Person(models.Model):
    def __unicode__(self):    
        return '{0}, {1}'.format(self.first, self.last)
    
    id = models.AutoField(db_column='PersonID',primary_key=True,verbose_name="Person ID")
    last = models.CharField(db_column='Last', max_length=30, blank=True)  # Field name made lowercase.
    first = models.CharField(db_column='First', max_length=40, blank=True)  # Field name made lowercase.
    middle = models.CharField(db_column='Middle', max_length=20, blank=True)  # Field name made lowercase.
    chinese = models.CharField(db_column='Chinese', max_length=20, blank=True)  # Field name made lowercase.
    sex = models.CharField(db_column='Sex', max_length=2, blank=True)  # Field name made lowercase.
    role = models.CharField(db_column='Role', max_length=4, blank=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, blank=True)  # Field name made lowercase.
    cphone = models.CharField(db_column='CPhone', max_length=510, blank=True)  # Field name made lowercase.
    wphone = models.CharField(db_column='WPhone', max_length=40, blank=True)  # Field name made lowercase.
    wfax = models.CharField(db_column='WFax', max_length=40, blank=True)  # Field name made lowercase.
    waddress = models.CharField(db_column='Waddress', max_length=100, blank=True)  # Field name made lowercase.
    worship = models.CharField(db_column='Worship', max_length=4, blank=True, help_text="C -- Cantonese, E -- English, M -- Mandarin")  # Field name made lowercase.
    fellowship = models.CharField(db_column='Fellowship', max_length=50, blank=True)  # Field name made lowercase.
    fellowship2 = models.CharField(db_column='Fellowship2', max_length=50, blank=True)  # Field name made lowercase.
    baptized = models.CharField(db_column='Baptized', max_length=4, blank=True, help_text="Y -- Yes, N -- No, YM -- MCCC Baptized, U -- Unknown")  # Field name made lowercase.
    bapday = models.CharField(db_column='BapDay', max_length=510, blank=True)  # Field name made lowercase.
    category = models.CharField(db_column='Category', max_length=4, blank=True)  # Field name made lowercase.
    birthday = models.DateField(db_column='Birthday', blank=True, null=True)  # Field name made lowercase.
    anniday = models.DateField(db_column='AnniDay', blank=True, null=True)  # Field name made lowercase.
    member = models.CharField(db_column='Member', max_length=2, blank=True, help_text="Y -- Active, N -- No, I -- Inactive, J -- Jr Member, U -- Unknown, D -- Deceased")  # Field name made lowercase.
    memday = models.DateField(db_column='MemDay', blank=True, null=True)  # Field name made lowercase.
    comment = models.TextField(db_column='Comment', blank=True, null=True)  # Field name made lowercase.
    family = models.ForeignKey(Family,db_column='FamilyID',related_name="persons")

    class Meta:
        managed = False
        db_table = 'MCCC_Person'
