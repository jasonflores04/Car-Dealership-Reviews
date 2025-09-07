"""
ASGI config for djangoproj project

It exposes the ASGI callable as a module-level variable named ``application``

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' command-line interface
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproj.settings')

# The ASGI application callable used by ASGI servers
application = get_asgi_application()
