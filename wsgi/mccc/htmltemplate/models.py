from django.db import models


class HtmlTemplate(models.Model):
    name = models.CharField(max_length=100,unique=True,)
    description = models.CharField(max_length=200,blank=True,null=True,)
    content = models.TextField(blank=True, null=True,)

    class Meta:
        db_table = 'html_template'
