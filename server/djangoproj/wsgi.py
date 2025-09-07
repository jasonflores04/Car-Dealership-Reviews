"""
WSGI config for djangoproj project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the 'wsgi' CLI utility
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')

# The WSGI application callable used by WSGI servers
application = get_wsgi_application()