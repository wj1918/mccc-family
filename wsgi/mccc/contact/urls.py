from django.conf.urls import include, url
from .views import ContactView
from .views import ContactView
from .views import EmailPreviewView
urlpatterns = [
    url(r"^/", ContactView.as_view(), name="update"),
    url(r"^preview/", EmailPreviewView.as_view(), name="preview"),
]
