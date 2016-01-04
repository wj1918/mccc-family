from django.conf.urls import include, url
from .views import EmailPreviewView
urlpatterns = [
    url(r"^preview/", EmailPreviewView.as_view(), name="preview"),
]
