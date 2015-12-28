from django.db import models
from django.contrib.auth.models import User


class EmailSession(models.Model):
    user = models.OneToOneField(User)
    state = models.CharField(max_length=200,unique=True,)
    token = models.TextField(null=True,)

    class Meta:
        db_table = 'MCCC_Email_Session'
