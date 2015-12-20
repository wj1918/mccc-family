
from django.contrib.admin import AdminSite
from models import McccLibrary
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.shortcuts import redirect

class LibrarySite(AdminSite):
    site_header = 'Library'

    def login(self, request, extra_context=None):
        return redirect('%s?next=%s' % (reverse('home'), request.REQUEST.get('next', '')))

class McccLibraryAdmin(admin.ModelAdmin):

    list_display = ('title', 'author', 'itemtype','classnumber','volume','clutternumber', 'inputdate')
    list_filter = ['itemtype','application','classnumber',]
   
    readonly_fields = ('itemtype','classnumber','volume','author','title','autocounter','clutternumber', 'keeper','keeperindex', 'inputdate', 'application')
    search_fields = ('classnumber', 'author','title')
    ordering = ['title']

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def get_actions(self, request):
        actions = super(McccLibraryAdmin, self).get_actions(request)
        if request.user.is_superuser:
            return actions
        else:
            return None

library_site = LibrarySite(name='library')
library_site.register(McccLibrary,McccLibraryAdmin)
