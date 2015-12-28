from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from .authhelper import get_signin_url

def login(request):
  redirect_uri = request.build_absolute_uri(reverse('outlook:outlook'))
  sign_in_url = get_signin_url(redirect_uri)
  return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')

def outlook(request):
  return HttpResponse('gettoken view')