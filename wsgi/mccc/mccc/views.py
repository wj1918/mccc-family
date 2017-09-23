#from social.apps.django_app.views import complete as django_complete
from django.http import HttpResponse
import datetime
from cipher import aes_cipher
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from mccc import settings

#def mccc_complete(request, backend, *args, **kwargs):
    # call the original view
#    import pdb; pdb.set_trace()
#    response = django_complete(request, backend, *args, **kwargs)
#    return response

@user_passes_test(lambda u: u.is_superuser, login_url='/')
def database(request):
    credential=aes_cipher.encrypt("%s:%s" % (settings.DATABASES['default']['USER'], settings.DATABASES['default']['PASSWORD']) ) 
    return redirect('/phpMyAdmin/signon.php?c='+credential)