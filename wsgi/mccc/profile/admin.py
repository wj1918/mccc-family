# admin.py
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import string_concat, ugettext as _, ungettext
from django.http import Http404, HttpResponseRedirect
from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from models import UserProfile
from django.contrib.admin import AdminSite
from django.conf import settings
from django.contrib.auth.decorators import login_required

from functools import update_wrapper
from django.utils import six
from models import ProfileFamily
from models import ProfilePerson
import autocomplete_light

# admin site cusrom user admin
class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1
    raw_id_fields = ("person",)

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]
#    form = autocomplete_light.modelform_factory(ProfilePerson, exclude = [])

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

#The raw_id_fields widget shows a magnifying glass button next to the field which allows users to search for and select a value
class ProfilePersonAdminPicker(admin.ModelAdmin):
    list_display = ('id','last','first','chinese','sex','email', 'cphone','role','birthday',)
    search_fields = ['last','first','chinese','email', 'cphone',]

admin.site.register(ProfilePerson, ProfilePersonAdminPicker)

class ProfilePersonInline(admin.StackedInline):
    exclude =['role',]
    model = ProfilePerson
    extra = 0
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request);

    def has_delete_permission(self, request, obj=None):
        return False

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff

# Below is for profile site

class ProfileFamilyAdmin(admin.ModelAdmin):
    inlines = [ProfilePersonInline]
    exclude =['user','status']
    
    def __init__(self, model, admin_site):
        self.model = model
        self.opts = model._meta
        self.admin_site = admin_site
        super(admin.ModelAdmin, self).__init__()
    
    def get_urls(self):
        from django.conf.urls import url
        
        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return login_required(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        my_urls=[
            url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
            url(r'^update/$', wrap(self.change_view), name='change_family'),
        ]
        return my_urls

    def change_view(self, request):
        objectid='%s' % request.user.userprofile.person.family.id
        return super(ProfileFamilyAdmin,self).changeform_view(request, objectid)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        #TODO 
        # return obj is None or obj.userprofile.user==request.user;
        return True

    def has_delete_permission(self, request, obj=None):
        return False;

    def has_module_permission(self, request):
        return True
        
    def i18n_javascript(self, request):
        if settings.USE_I18N:
            from django.views.i18n import javascript_catalog
        else:
            from django.views.i18n import null_javascript_catalog as javascript_catalog
        return javascript_catalog(request, packages=['profile'])

    def response_change(self, request, obj):
        """
        Determines the HttpResponse for the change_view stage.
        """
        opts = self.model._meta

        msg_dict = {'name': force_text(opts.verbose_name), 'obj': force_text(obj)}
        if "_continue" in request.POST:
            msg = _('The %(name)s "%(obj)s" was changed successfully. You may edit it again below.') % msg_dict
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = request.path
            return HttpResponseRedirect(redirect_url)
        else:
            msg = _('The %(name)s "%(obj)s" was changed successfully.') % msg_dict
            self.message_user(request, msg, messages.SUCCESS)
            post_url = reverse('home')
            return HttpResponseRedirect(post_url)

class ProfileSite(AdminSite):
    site_header = 'User Profile'

    def get_urls(self):
        model_admin= self._registry[ProfileFamily]
        return model_admin.get_urls()


profile_site = ProfileSite(name="profile")
profile_site.register(ProfileFamily, ProfileFamilyAdmin)
