"""
from django.conf.urls import patterns, url 
from .views import login 
from .views import outlook 
urlpatterns = patterns('', 
  url(r'^gmail/start/$', login, name='gmail-start'), 
  url(r'^gmail/complete/$', outlook, name='gmail-complete'),
) 
"""

"""copy from social.apps.django_app.urls"""
"""URLs module"""

from django.conf import settings
from django.conf.urls import patterns, url
from social.utils import setting_name

extra = getattr(settings, setting_name('TRAILING_SLASH'), True) and '/' or ''

urlpatterns = patterns('oauthemail.views',
    # authentication / association
    url(r'^login/(?P<backend>[^/]+){0}$'.format(extra), 'auth',
        name='begin'),
    url(r'^complete/(?P<backend>[^/]+){0}$'.format(extra), 'complete',
        name='complete'),
    # disconnection
    url(r'^disconnect/(?P<backend>[^/]+){0}$'.format(extra), 'disconnect',
        name='disconnect'),
    url(r'^disconnect/(?P<backend>[^/]+)/(?P<association_id>[^/]+){0}$'
            .format(extra), 'disconnect', name='disconnect_individual'),
    url(r'^show_login/$', "show_login"),
    url(r'^test_email/$', "test_email"),

)
