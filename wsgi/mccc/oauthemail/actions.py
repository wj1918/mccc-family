from django.http import HttpResponse, HttpResponseRedirect
from social.p3 import quote
from social.utils import sanitize_redirect, user_is_authenticated, \
                         user_is_active, partial_pipeline_data, setting_url


def do_auth(backend, redirect_name='next'):
    data = backend.strategy.request_data(merge=False)

    for field_name in backend.setting('FIELDS_STORED_IN_SESSION', []):
        if field_name in data:
            backend.strategy.session_set(field_name, data[field_name])
    return backend.start()

def do_complete(backend, login, user=None, redirect_name='next',
                *args, **kwargs):

    data = backend.strategy.request_data()
    user = backend.complete(user=user, *args, **kwargs)
    return HttpResponse("Thank You!")

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
