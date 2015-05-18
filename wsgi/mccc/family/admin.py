from django.contrib import admin

# Register your models here.

from family.models import Person
from family.models import Family
from django.utils.translation import ugettext_lazy as _
from django.contrib.admin import SimpleListFilter

from django.contrib.admin import SimpleListFilter
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

def add_link_field(target_model = None, field = '', app='', field_name='link',
                   link_text=unicode):
    def add_link(cls):
        reverse_name = target_model or cls.model.__name__.lower()
        def link(self, instance):
            app_name = app or instance._meta.app_label
            reverse_path = "admin:%s_%s_change" % (app_name, reverse_name)
            link_obj = getattr(instance, field, None) or instance
            url = reverse(reverse_path, args = (link_obj.id,))
            return mark_safe("<a href='%s'>%s</a>" % (url, link_text(link_obj)))
        link.allow_tags = True
        link.short_description = reverse_name 
        setattr(cls, field_name, link)
        cls.readonly_fields = list(getattr(cls, 'readonly_fields', [])) + \
            [field_name]
        return cls
    return add_link
    
class PersonInline(admin.StackedInline):
    model = Person
    extra = 0

class FamilyAdmin(admin.ModelAdmin):
    list_display = ('id','address','city','state','zip','status', 'home1','home2', 'homefax')
    list_filter = ['status','city','state']
    search_fields = ['id','address','city','home1']
    inlines = [PersonInline]
        
@add_link_field('family','family',field_name='link2')
class PersonAdmin(admin.ModelAdmin):
    list_display = ('id','last','first','middle','chinese','sex','role','link2','get_family_phone','email','cphone','wphone','worship','fellowship','fellowship2','baptized','bapday','category','birthday','member','memday','get_family_id','get_family_status')
    list_filter = ['fellowship','fellowship2','worship','baptized','member', 'family__status', 'family__city',]
    search_fields = ['last','first','chinese','email','comment', "family__address", "family__city", "family__state", "family__zip","family__home1","family__home2","family__homefax",]
    raw_id_fields = ("family",)
    
    def get_family_status(self, obj):
        return obj.family.status
    get_family_status.short_description = 'Family Status'
    get_family_status.admin_order_field = 'family__status'

    def get_family_id(self, obj):
        return obj.family.id
    get_family_id.short_description = 'Family Id'
    get_family_id.admin_order_field = 'family__id'

    def get_family_address(self, obj):
        list1 = [obj.family.address, obj.family.city, obj.family.state, obj.family.zip]
        faddress =[x for x in list1 if x is not None]
        return u','.join(faddress).encode('utf-8').strip()
        
    get_family_address.short_description = 'Family Address'
    get_family_address.admin_order_field = 'family__address'

    def get_family_phone(self, obj):
        list1 = [obj.family.home1, obj.family.home2, obj.family.homefax]
        fphones =[x for x in list1 if x is not None]
        return u' '.join(fphones).encode('utf-8').strip()
    get_family_phone.short_description = 'Family Phone'
    get_family_phone.admin_order_field = 'family__home1s'

admin.site.register(Family,FamilyAdmin)
admin.site.register(Person,PersonAdmin)
