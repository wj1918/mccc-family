from django.db import models
from django.contrib.auth.models import User


class EmailSession(models.Model):
    user = models.ForeignKey(User)
    state = models.CharField(max_length=200,)
    code = models.CharField(max_length=200,)
    session_state = models.CharField(max_length=200, null=True,)
    backend_name = models.CharField(max_length=20, null=True,)
    email = models.CharField(max_length=100, null=True,)
    display_name = models.CharField(max_length=100, null=True,)
    token_type = models.CharField(max_length=100, null=True,)
    access_token = models.CharField(max_length=200, null=True,)

    class Meta:
        db_table = 'MCCC_Email_Session'
