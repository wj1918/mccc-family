import unicodecsv
from functools import wraps
from collections import OrderedDict
from django.db.models import FieldDoesNotExist
from urllib.parse import quote
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import admin
from django.contrib.admin import AdminSite
from singledispatch import singledispatch  # pip install singledispatch

from .models import McccDir
from contact.utils import create_dir_update
from django.contrib.admin.views.main import ChangeList
import collections

def prep_field(obj, field):
    """
    (for download_as_csv action)
    Returns the field as a unicode string. If the field is a callable, it
    attempts to call it first, without arguments.
    """
    if '__' in field:
        bits = field.split('__')
        field = bits.pop()

        for bit in bits:
            obj = getattr(obj, bit, None)

            if obj is None:
                return ""

    attr = getattr(obj, field)
    output = attr() if isinstance(attr, collections.Callable) else attr
    return str(output).encode('utf-8') if output is not None else ""


@singledispatch
def download_as_csv(modeladmin, request, queryset):
    """
    Generic csv export admin action.

    Example:

        class ExampleModelAdmin(admin.ModelAdmin):
            raw_id_fields = ('field1',)
            list_display = ('field1', 'field2', 'field3',)
            actions = [download_as_csv,]
            download_as_csv_fields = [
                'field1',
                ('foreign_key1__foreign_key2__name', 'label2'),
                ('field3', 'label3'),
            ],
            download_as_csv_header = True
    """
    fields = getattr(modeladmin, 'download_as_csv_fields', None)
    exclude = getattr(modeladmin, 'download_as_csv_exclude', None)
    header = getattr(modeladmin, 'download_as_csv_header', True)
    verbose_names = getattr(modeladmin, 'download_as_csv_verbose_names', True)

    opts = modeladmin.model._meta

    def fname(field):
        if verbose_names:
            return str(field.verbose_name).capitalize()
        else:
            return field.name

    # field_names is a map of {field lookup path: field label}
    if exclude:
        field_names = OrderedDict(
            (f.name, fname(f)) for f in opts.fields if f not in exclude
        )
    elif fields:
        field_names = OrderedDict()
        for spec in fields:
            if isinstance(spec, (list, tuple)):
                field_names[spec[0]] = spec[1]
            else:
                try:
                    f, _, _, _ = opts.get_field_by_name(spec)
                except FieldDoesNotExist:
                    field_names[spec] = spec
                else:
                    field_names[spec] = fname(f)
    else:
        field_names = OrderedDict(
            (f.name, fname(f)) for f in opts.fields
        )

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
            str(opts).replace('.', '_')
        )

    # writer = csv.writer(response)
    writer = unicodecsv.writer(response, encoding='utf-8')
    

    if header:
        writer.writerow(list(field_names.values()))

    for obj in queryset:
        writer.writerow([prep_field(obj, field) for field in list(field_names.keys())])
    return response

download_as_csv.short_description = "Download selected objects as CSV file"

@download_as_csv.register(str)
def _(description):
    """
    (overridden dispatcher)
    Factory function for making a action with custom description.

    Example:

        class ExampleModelAdmin(admin.ModelAdmin):
            raw_id_fields = ('field1',)
            list_display = ('field1', 'field2', 'field3',)
            actions = [download_as_csv("Export Special Report"),]
            download_as_csv_fields = [
                'field1',
                ('foreign_key1__foreign_key2__name', 'label2'),
                ('field3', 'label3'),
            ],
            download_as_csv_header = True
    """
    @wraps(download_as_csv)
    def wrapped_action(modeladmin, request, queryset):
        return download_as_csv(modeladmin, request, queryset)
    wrapped_action.short_description = description
    return wrapped_action

class MemberSite(AdminSite):
    site_header = 'Member'

    def login(self, request, extra_context=None):
        return redirect('%s?next=%s' % (reverse('home'), request.REQUEST.get('next', '')))


class MemberChangeList(ChangeList):
    def __init__(self, *args, **kwargs):
        super(MemberChangeList, self).__init__(*args, **kwargs)
        self.title = "Search member"

        
class McccDirAdmin(admin.ModelAdmin):
    list_display = ('last_nm','first_nm','chinese_nm','wf_first','wf_chinese_nm','home_phone', 'cell_phone','address', 'worship')
    list_filter = ['worship']
    readonly_fields = ('family_id','last_nm','first_nm','chinese_nm','wf_first','wf_chinese_nm','home_phone', 'cell_phone','address', 'worship')
    search_fields = ('last_nm','first_nm','chinese_nm','wf_first','wf_chinese_nm','home_phone', 'cell_phone','address', 'worship')
    ordering = ['last_nm']

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def create_invite(self, request, queryset):
        rows_updated = create_dir_update(queryset)
        if rows_updated == 1:
            message_bit = "1 update invite was"
        else:
            message_bit = "%s invite were" % rows_updated
        self.message_user(request, "%s successfully created." % message_bit)
    create_invite.short_description = "Create directory update."

    actions = [download_as_csv("Download selected objects as CSV file"), create_invite,]
    download_as_csv_fields=[
        'last_nm',
        'first_nm', 
        'chinese_nm',
        'wf_first', 
        'wf_chinese_nm',
        'home_phone', 
        'cell_phone',
        'address', 
        'worship',
    ]
    download_as_csv_header = True

    def get_actions(self, request):
        actions = super(McccDirAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
        else:
            return None

    def get_changelist(self, request, **kwargs):
        return MemberChangeList
        
member_site = MemberSite(name='member')
member_site.site_header = 'MCCC Member Directory'
member_site.site_title ='MCCC Member Directory'
member_site.register(McccDir,McccDirAdmin)
