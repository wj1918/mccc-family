from social.apps.django_app.views import complete as django_complete

def mccc_complete(request, backend, *args, **kwargs):
    # call the original view
#    import pdb; pdb.set_trace()
    response = django_complete(request, backend, *args, **kwargs)
    # return the response
    return response
