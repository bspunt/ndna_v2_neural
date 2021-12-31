"""
WSGI config for mysite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os
import time 
import sys

from django.core.wsgi import get_wsgi_application

sys.path.append('/var/www/django_app/mysite') 
sys.path.append('/usr/lib/python3.5')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')

application = get_wsgi_application()
