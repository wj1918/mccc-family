
from django.contrib import admin
from .models import HtmlTemplate


class HtmlTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'name','description', 'content',)
    search_fields = ('name','description',)
    ordering = ['name']

admin.site.register(HtmlTemplate,HtmlTemplateAdmin)
