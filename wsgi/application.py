#!/usr/bin/env python

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mccc.settings'
sys.path.append(os.path.join(os.environ['OPENSHIFT_REPO_DIR'], 'wsgi', 'mccc'))
virtenv = os.environ['OPENSHIFT_RUNTIME_DIR'] + '/venv/'
os.environ['PYTHON_EGG_CACHE'] = os.path.join(virtenv, 'lib/python2.7/site-packages')
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except:
    pass

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
