from django.db import models


class HtmlTemplate(models.Model):
    name = models.CharField(max_length=100,unique=True,)
    description = models.CharField(max_length=200,null=True,)
    content = models.TextField(null=True,)

    class Meta:
        db_table = 'MCCC_Html_Template'
