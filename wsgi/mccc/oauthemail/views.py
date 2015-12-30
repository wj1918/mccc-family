"""
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from .authhelper import get_signin_url

#def login(request):
#  redirect_uri = request.build_absolute_uri(reverse('outlook:outlook'))
#  sign_in_url = get_signin_url(redirect_uri)
#  return HttpResponse('<a href="' + sign_in_url +'">Click here to sign in and view your mail</a>')
  
def login(request):
  return HttpResponseRedirect(reverse("social:begin", args=("azuread-oauth2",)))

def outlook(request):
  return HttpResponse('gettoken view')
  
"""  

from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from django.core import mail
from django.contrib.auth import login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.http import require_POST
from django.views.decorators.cache import never_cache
from django.utils.html import escape

from .actions import do_auth, do_complete, do_disconnect
from .utils import psa, send_email


NAMESPACE = 'oauthemail'


@never_cache
@psa('{0}:complete'.format(NAMESPACE))
def auth(request, backend):
    return do_auth(request.backend, redirect_name=REDIRECT_FIELD_NAME)


@login_required
@never_cache
@csrf_exempt
@psa('{0}:complete'.format(NAMESPACE))
def complete(request, backend, *args, **kwargs):
    """Authentication complete view"""
    return do_complete(request.backend, _do_login, request.user,
                       redirect_name=REDIRECT_FIELD_NAME, *args, **kwargs)


@never_cache
@login_required
@psa()
@require_POST
@csrf_protect
def disconnect(request, backend, association_id=None):
    """Disconnects given backend from current logged in user."""
    return do_disconnect(request.backend, request.user, association_id,
                         redirect_name=REDIRECT_FIELD_NAME)


def _do_login(backend, user, social_user):
    user.backend = '{0}.{1}'.format(backend.__module__,
                                  backend.__class__.__name__)
    login(backend.strategy.request, user)
    if backend.setting('SESSION_EXPIRATION', False):
        # Set session expiration date if present and enabled
        # by setting. Use last social-auth instance for current
        # provider, users can associate several accounts with
        # a same provider.
        expiration = social_user.expiration_datetime()
        if expiration:
            try:
                backend.strategy.request.session.set_expiry(
                    expiration.seconds + expiration.days * 86400
                )
            except OverflowError:
                # Handle django time zone overflow
                backend.strategy.request.session.set_expiry(None)

@never_cache
@csrf_protect
@login_required
def show_login(request):
  gmail_sign_in_url = reverse("oauthemail:begin", args=("gmail-oauth2",))
  hotmail_sign_in_url = reverse("oauthemail:begin", args=("hotmail-oauth2",))

  return HttpResponse('<a href="' + gmail_sign_in_url +'">Click here to sign in gmail</a> '+
    '<p> ' + '<a href="' + hotmail_sign_in_url +'">Click here to sign in hotmail</a> ')


@never_cache
@csrf_protect
@login_required
def test_email(request):

    with mail.get_connection("oauthemail.smtp.OauthEmailBackend", user=request.user) as connection:
        mail.EmailMessage('Subject here', 
            'Here is the message.', 
            to=['Jun Wang<wj1918@hotmail.com>'], connection=connection).send()    
    return HttpResponse("Email Sent OK.")
