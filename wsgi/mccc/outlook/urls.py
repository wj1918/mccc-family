from django.conf.urls import patterns, url 
from .views import login 
from .views import outlook 

urlpatterns = patterns('', 
  url(r'^login/$', login, name='login'), 
  url(r'^outlook/$', outlook, name='outlook'),
) 