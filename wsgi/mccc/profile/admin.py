# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.admin import AdminSite
from django.conf import settings

from functools import update_wrapper
from django.utils import six
from models import ProfileFamily
from models import ProfilePerson

class ProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1
    raw_id_fields = ("family",)

class CustomUserAdmin(UserAdmin):
    inlines = [ProfileInline,]

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

class UserProfileAdmin(admin.ModelAdmin):
    exclude =['user',]

    def get_queryset(self, request):
        qs = super(UserProfileAdmin, self).get_queryset(request)
        return qs.filter(user=request.user)
        
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        #import pdb; pdb.set_trace()
        #return not obj and obj.user==request.user
        return obj is None or obj.user==request.user ;

    def has_delete_permission(self, request, obj=None):
        return False;

    def has_module_permission(self, request):
        return True

#admin.site.register(UserProfile,UserProfileAdmin)

class ProfilePersonInline(admin.StackedInline):
    model = ProfilePerson
    extra = 0
    
    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return self.has_module_permission(request);

    def has_delete_permission(self, request, obj=None):
        return self.has_module_permission(request);

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff

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
                return self.admin_site.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        
        my_urls=[
            url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),
            url(r'^update/$', wrap(self.change_view), name='%s_%s_update' % info),
        ]
        return my_urls

    def change_view(self, request):
        objectid='%s' % request.user.userprofile.family.id
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

class ProfileSite(AdminSite):
    site_header = 'User Profile'

    def get_urls(self):
        model_admin= self._registry[ProfileFamily]
        return model_admin.get_urls()

profile_site = ProfileSite(name="profile")
profile_site.register(ProfileFamily,ProfileFamilyAdmin)

