from django.conf.urls import include, url
from django.contrib import admin
from children.admin import children_site
from . import views

urlpatterns = [
    url(r'^attendancesheet/([A-Za-z0-9\+]+)/([0-9]+)/([0-9]+)/$', views.attendancesheet),
    url(r'^children/', include(children_site.urls)),
    
]
