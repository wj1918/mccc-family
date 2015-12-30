from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.utils.html import escape
from social.p3 import quote
from social.utils import sanitize_redirect, user_is_authenticated, \
                         user_is_active, partial_pipeline_data, setting_url
from .utils import save_oauth_session

def do_auth(backend, redirect_name='next'):
#    return HttpResponse(escape(repr(data)))
    """ backend.start() was overwritten in GmailOAuth2 """        
    return backend.start()
    
"""
                \_ self.strategy.redirect(self.auth_url())
                   \_ BaseOAuth2.auth_url()
                      \_ self.get_or_create_state()
"""

def do_complete(backend, login, user, redirect_name='next',
                *args, **kwargs):

    backend.complete(user=user, *args, **kwargs)
    """
        Function call sequence of backend.complete:
        
         \_backend.base.complete(self, *args, **kwargs)
            \_ BaseOAuth2.auth_complete(*args, **kwargs)
               | validate_state()
               | process_error(self.data)
               | exchange code for token    
                \_ oauth.do_auth(self, access_token, *args, **kwargs)
                  | Finish the auth process once the access_token was retrieved
                  | following is overwritren in GmailOAuth2
                  | pass user data and access token to next function
                   \_  self.strategy.authenticate(*args, **kwargs)
                   \_ backend.base.authenticate(*args, **kwargs)
                      |Authenticate user using social credentials
                      |overwritten by next function
                   \_ oauthemail.backends.google.GmailOAuth2.authenticate         

    """
    data = backend.data
    if data["email"] == user.email:
        data.update({
            'host':backend.setting('HOST'),
            'port':backend.setting('PORT'),
            })    
        save_oauth_session(user, backend.name, data)
        return HttpResponse("Login successfully! Your email is '{0} &lt;{1}&gt;' ".format(data["display_name"],data["email"]) )
    else:
        return HttpResponse("Invalid email account {0}, Please login to {1} ".format(data["email"], user.email))
        
def do_disconnect(backend, user, association_id=None, redirect_name='next',
                  *args, **kwargs):
    partial = partial_pipeline_data(backend, user, *args, **kwargs)
    if partial:
        xargs, xkwargs = partial
        if association_id and not xkwargs.get('association_id'):
            xkwargs['association_id'] = association_id
        response = backend.disconnect(*xargs, **xkwargs)
    else:
        response = backend.disconnect(user=user, association_id=association_id,
                                      *args, **kwargs)

    if isinstance(response, dict):
        response = backend.strategy.redirect(
            backend.strategy.request_data().get(redirect_name, '') or
            backend.setting('DISCONNECT_REDIRECT_URL') or
            backend.setting('LOGIN_REDIRECT_URL')
        )
    return response
