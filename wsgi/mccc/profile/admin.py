# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from models import UserProfile
from django.contrib.admin import AdminSite

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

admin.site.register(UserProfile,UserProfileAdmin)

class ProfilePersonInline(admin.StackedInline):
    model = ProfilePerson
    extra = 0
    def has_permission(self, request, obj):
        #TODO
        #return obj is not None and obj.userprofile.user==request.user;
        return True;
    
    def has_add_permission(self, request):
        return self.has_module_permission(request)

    def has_change_permission(self, request, obj=None):
        return self.has_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return self.has_permission(request, obj)

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff


class ProfileFamilyAdmin1(admin.ModelAdmin):
    list_display = ('id','address','city','state','zip','status', 'home1','home2', 'homefax')
    list_filter = ['status','city','state']
    search_fields = ['id','address','city','home1']
    inlines = [ProfilePersonInline]
    exclude =['user',]

admin.site.register(ProfileFamily, ProfileFamilyAdmin1)

class ProfileFamilyAdmin(admin.ModelAdmin):
    list_display = ('id','address','city','state','zip','status', 'home1','home2', 'homefax')
    list_filter = ['status','city','state']
    search_fields = ['id','address','city','home1']
    inlines = [ProfilePersonInline]
    exclude =['user',]
    #def __init__(self, model, admin_site):
    #    self.model = model
    #    self.opts = model._meta
    #    self.admin_site = admin_site
    #    super(admin.ModelAdmin, self).__init__()
    
    def get_urls(self):
        from django.conf.urls import url
        
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            wrapper.model_admin = self
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.model_name
        
        urls = super(ProfileFamilyAdmin, self).get_urls()
        
        my_urls=[
            url(r'^/$', wrap(self.change_view), name='%s_%s_update' % info),
        ]
        return my_urls + urls

    def change_view(self, request):
        return super(ProfileFamilyAdmin,self).changeform_view(request, "975")

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

class ProfileSite(AdminSite):
    site_header = 'User Profile'
    def get_urls(self):
        from django.conf.urls import url, include

        def wrap(view, cacheable=False):
            def wrapper(*args, **kwargs):
                return self.admin_view(view, cacheable)(*args, **kwargs)
            return update_wrapper(wrapper, view)


        urlpatterns = [
            url(r'^$', wrap(self.index), name='index'),
            url(r'^jsi18n/$', wrap(self.i18n_javascript, cacheable=True), name='jsi18n'),

            ]

        # Add in each model's views
        for model, model_admin in six.iteritems(self._registry):
            urlpatterns += [
#                url(r'^%s/%s/' % (model._meta.app_label, model._meta.model_name), include(model_admin.urls)),
                url(r'^update/$', wrap(model_admin.change_view)),

            ]

        return urlpatterns
        
    def index1(request):
        return  HttpResponseNotFound('<h1>Page not found</h1>')


profile_site = ProfileSite(name="profile")
#pfa=ProfileFamilyAdmin(ProfileFamily,profile_site)
#profile_site = AdminSite(name="profile")
profile_site.register(ProfileFamily,ProfileFamilyAdmin)
#profile_site.register(ProfilePerson)

