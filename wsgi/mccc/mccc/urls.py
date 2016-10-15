from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from account.views import LogoutView
from django.views.generic.base import RedirectView
from member.admin import member_site
from children.admin import children_site
from library.admin import library_site
from profile.admin import profile_site
from children.urls import urlpatterns as children_urlpatterns
from .views import database;
from contact.views import ContactUpdateView
from contact.views import SignupConfirmView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"^$", TemplateView.as_view(template_name="homepage.html"), name="home"),
    url(r"^accounts/login/$", RedirectView.as_view(url='/')),
    url(r"^accounts/logout/$", RedirectView.as_view(url='/')),
    url(r"^admin/login/$", RedirectView.as_view(url='/')),
    url(r"^admin/logout/$", RedirectView.as_view(url='/')),
    url(r'^admin/', include(admin.site.urls)),
    url(r"^account/social/", include("social.apps.django_app.urls", namespace="social")),
    url(r"^account/logout/$", LogoutView.as_view(), name="account_logout"),
    url(r'^member/', include(member_site.urls)),
    url(r'^library/', include(library_site.urls)),
    url(r'^myfamily/', include(profile_site.urls)),
    url(r'^database/', database),
#    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^contact/', include('contact.urls', namespace="contact")),
    url(r'^oauthemail/', include('oauthemail.urls', namespace="oauthemail")),
    url(r'^t/(?P<token>[^/]+)$', ContactUpdateView.as_view(), name='update_contact'),
    url(r'^s/(?P<token>[^/]+)$', SignupConfirmView.as_view(), name='signup_confirm'),
    
    
    
)

urlpatterns += children_urlpatterns
urlpatterns += staticfiles_urlpatterns()

admin.site.site_header = 'Administration'
admin.site.site_title ='Site admin'

children_site.site_header = 'Administration'
children_site.site_title ='Site admin'

library_site.site_header = 'Administration'
library_site.site_title ='Site admin'
