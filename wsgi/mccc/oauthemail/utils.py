import warnings

from functools import wraps
import base64
import smtplib

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404

from social.utils import setting_name, module_member
from social.exceptions import MissingBackend
from social.strategies.utils import get_strategy
from social.backends.utils import get_backend
from .models import EmailSession

"""
OAUTHEMAIL_BACKENDS = [
    "oauthemail.backends.google.GmailOAuth2",
    "oauthemail.backends.live.HotmailOAuth2",
]

"""
BACKENDS = settings.OAUTHEMAIL_BACKENDS
STRATEGY = getattr(settings, setting_name('STRATEGY'),
                   'social.strategies.django_strategy.DjangoStrategy')
STORAGE = getattr(settings, setting_name('STORAGE'),
                  'social.apps.django_app.default.models.DjangoStorage')
Strategy = module_member(STRATEGY)
Storage = module_member(STORAGE)


def load_strategy(request=None):
    return get_strategy(STRATEGY, STORAGE, request)


def load_backend(strategy, name, redirect_uri):
    Backend = get_backend(BACKENDS, name)
    return Backend(strategy, redirect_uri)


def psa(redirect_uri=None, load_strategy=load_strategy):
    def decorator(func):
        @wraps(func)
        def wrapper(request, backend, *args, **kwargs):
            uri = redirect_uri
            if uri and not uri.startswith('/'):
                uri = reverse(redirect_uri, args=(backend,))
            request.social_strategy = load_strategy(request)
            # backward compatibility in attribute name, only if not already
            # defined
            if not hasattr(request, 'strategy'):
                request.strategy = request.social_strategy

            try:
                request.backend = load_backend(request.social_strategy,
                                               backend, uri)
            except MissingBackend:
                raise Http404('Backend not found')
            return func(request, backend, *args, **kwargs)
        return wrapper
    return decorator


def setting(name, default=None):
    try:
        return getattr(settings, setting_name(name))
    except AttributeError:
        return getattr(settings, name, default)


class BackendWrapper(object):
    # XXX: Deprecated, restored to avoid session issues
    def authenticate(self, *args, **kwargs):
        return None

    def get_user(self, user_id):
        return Strategy(storage=Storage).get_user(user_id)


def strategy(*args, **kwargs):
    warnings.warn('@strategy decorator is deprecated, use @psa instead')
    return psa(*args, **kwargs)


def save_oauth_session(user, backend_name, data):

    ess=EmailSession.objects.filter(user=user)  
    es =ess[0]  if ess.count()>0 else EmailSession()
    
    es.user=user
    es.backend_name=backend_name
    es.state=data["state"]
    es.session_state=data["session_state"]
    es.code=data["code"]
    es.email=data["email"]
    es.display_name=data["display_name"]
    es.token_type=data["token_type"]
    es.access_token=data["access_token"]
    es.host=data["host"]
    es.port=data["port"]
    es.save()

def send_email(user):
    es=EmailSession.objects.get(user=user)
    auth_string=GenerateOAuth2String(user.email,es.access_token,base64_encode=False)
    TestSmtpAuthentication(user.email,auth_string)
    
    return auth_string

def get_user_auth_info(user):
    es=EmailSession.objects.get(user=user)
    auth_string = 'user=%s\1auth=Bearer %s\1\1' % (user.email, es.access_token)
    return {'auth_string':auth_string, "host": es.host, "port":es.port } 

def GenerateOAuth2String(username, access_token, base64_encode=True):
  """Generates an IMAP OAuth2 authentication string.

  See https://developers.google.com/google-apps/gmail/oauth2_overview

  Args:
    username: the username (email address) of the account to authenticate
    access_token: An OAuth2 access token.
    base64_encode: Whether to base64-encode the output.

  Returns:
    The SASL argument for the OAuth2 mechanism.
  """
  auth_string = 'user=%s\1auth=Bearer %s\1\1' % (username, access_token)
  if base64_encode:
    auth_string = base64.b64encode(auth_string)
  return auth_string



def TestSmtpAuthentication(user, auth_string):
  """Authenticates to SMTP with the given auth_string.
  Args:
    user: The Gmail username (full email address)
    auth_string: A valid OAuth2 string, not base64-encoded, as returned by
        GenerateOAuth2String.
  """
  smtp_conn = smtplib.SMTP('smtp.gmail.com', 587)
  smtp_conn.set_debuglevel(True)
  smtp_conn.ehlo('test')
  smtp_conn.starttls()
  smtp_conn.docmd('AUTH', 'XOAUTH2 ' + base64.b64encode(auth_string))
  
  msg = "YOUR Test MESSAGE!"
  smtp_conn.sendmail(user, "wj1918@hotmail.com", msg)
  smtp_conn.quit()

