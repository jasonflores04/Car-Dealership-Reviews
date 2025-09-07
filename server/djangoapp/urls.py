"""
URL Configuration
-----------------
This file defines URL patterns for the `djangoapp` application. Each path maps a 
specific route to its corresponding view function in `views.py`
"""
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

# App Name
app_name = 'djangoapp'

# Routes
urlpatterns = [
    # register: User registration page (`views.registration`)
    path(route='register', view=views.registration, name='register'),

    # login: User login page (`views.login_user`)
    path(route='login', view=views.login_user, name='login'),

    # logout: User logout functionality (`views.logout_request`)
    path(route='logout', view=views.logout_request, name='logout'),

    # get_cars: Fetch available cars (`views.get_cars`)
    path(route='get_cars', view=views.get_cars, name ='getcars'),

    # get_dealers: Fetch all dealerships (`views.get_dealerships`)
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers'),

    # get_dealers_by_state: Fetch dealerships filtered by state (`views.get_dealerships`)
    path(route='get_dealers/<str:state>', view=views.get_dealerships, name='get_dealers_by_state'),

    # dealer_details: Fetch details for a specific dealer by dealer_id (`views.get_dealer_details`)
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_details'),

    # dealer_reviews: Fetch reviews for a specific dealer (`views.get_dealer_reviews`)
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_details'),

    # add_review: Add a new review for a dealer (`views.add_review`)
    path(route='add_review', view=views.add_review, name='add_review'),

    # get_inventory: Fetch inventory for a dealer (`views.get_inventory`)
    path(route='get_inventory/<int:dealer_id>', view=views.get_inventory, name='get_inventory')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
