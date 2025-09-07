"""
Django Admin Configuration
--------------------------
This file registers the CarMake and CarModel models
with the Django admin site so they can be managed
through the built-in admin interface.
"""

from django.contrib import admin
from .models import CarMake, CarModel

# Register CarMake model in Django admin
admin.site.register(CarMake)

# Register CarModel model in Django admin
admin.site.register(CarModel)