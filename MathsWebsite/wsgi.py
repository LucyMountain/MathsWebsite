"""
WSGI config for MathsWebsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import sys

from MathsWebsite.settings import BASE_DIR, DJANGO_CONFIGURATION

if DJANGO_CONFIGURATION == 'Dev':
    sys.path.insert(0, os.path.join(BASE_DIR, 'venv/lib/site-packages'))
else:
    sys.path.insert(0, os.path.join(BASE_DIR, 'venv/lib/python3.10/site-packages'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'MathsWebsite.settings'


#def execfile(filename):
#    globals = dict(__file__=filename)
#    exec(open(filename).read(), globals)


#activate_this = os.path.join(BASE_DIR, 'venv/Scripts', 'activate_this.py')
#execfile(activate_this)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MathsWebsite.settings')

application = get_wsgi_application()
