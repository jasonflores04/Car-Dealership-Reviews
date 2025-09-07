"""
Views
-----
This file defines Django view functions for handling authentication, dealership 
data, reviews, cars, and inventory. Views interact with models, external APIs, 
and services, returning JSON responses for frontend consumption

Functions:
- get_cars: Returns a list of car makes and models; populates database if empty
- login_user: Authenticates a user and starts a session
- logout_request: Logs out the current user and clears session
- registration: Registers a new user account, or returns error if already registered
- get_dealerships: Fetches a list of dealerships (all or filtered by state)
- get_dealer_reviews: Fetches reviews for a specific dealer, with sentiment analysis
- get_dealer_details: Fetches details of a specific dealer
- add_review: Submits a review for a dealer (authenticated users only)
- get_inventory: Fetches dealer inventory, filterable by year, make, model, mileage, or price
"""
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review
from .restapis import get_request, analyze_review_sentiments, post_review, searchcars_request


def get_cars(request):
    """
    Returns all car makes and models from the database

    - If no CarMake records exist, calls `initiate()` to populate data
    - Uses `select_related` for efficient query joins with CarMake

    Returns:
        JsonResponse: {"CarModels": [{"CarModel": <name>, "CarMake": <make>}, ...]}
    """
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels":cars})

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    """
    Create a `login_request` view to handle sign in request

    Request Body (JSON):
        - userName (str): Username
        - password (str): Password

    Returns:
        JsonResponse: {"userName": <username>, "status": "Authenticated"} if login succeeds,
                      {"userName": <username>} otherwise
    """

    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

def logout_request(request):
    """
    Create a `logout_request` view to handle sign out request

    Returns:
        JsonResponse: {"userName": ""} with session cleared.
    """

    # Terminate user session
    logout(request) 
    # Return empty username
    data = {"userName":""} 
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    """
    Create a `registration` view to handle sign up request

    Request Body (JSON):
        - userName (str)
        - password (str)
        - firstName (str)
        - lastName (str)
        - email (str)

    Returns:
        JsonResponse: {"userName": <username>, "status": "Authenticated"} if created,
                      {"userName": <username>, "error": "Already Registered"} if user exists
    """
    context = {}
    # Load JSON data from the request body
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    email_exist = False
    try:
        # Check if user already exists
        User.objects.get(username=username)
        username_exist = True
    except:
        # If not, simply log this is a new user
        logger.debug("{} is new user".format(username))

    # If it is a new user
    if not username_exist:
        # Create user in auth_user table
        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,password=password, email=email)
        # Login the user and redirect to list page
        login(request, user)
        data = {"userName":username,"status":"Authenticated"}
        return JsonResponse(data)
    else :
        data = {"userName":username,"error":"Already Registered"}
        return JsonResponse(data)

def get_dealerships(request, state="All"):
    """
    Fetches dealerships from the backend service

    Args:
        state (str): Optional. If provided, filters dealerships by state.
                     Defaults to "All" for all dealerships

    Returns:
        JsonResponse: {"status": 200, "dealers": <list of dealerships>}
    """
    if(state == "All"):
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/"+state
    dealerships = get_request(endpoint)
    return JsonResponse({"status":200,"dealers":dealerships})

def get_dealer_reviews(request, dealer_id):
    """
    Fetches dealer reviews with sentiment analysis

    Args:
        dealer_id (int): The ID of the dealer

    Returns:
        JsonResponse: {"status": 200, "reviews": <list with sentiments>} if valid dealer_id,
                      {"status": 400, "message": "Bad Request"} otherwise
    """

    # if dealer id has been provided
    if(dealer_id):
        endpoint = "/fetchReviews/dealer/"+str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            print(response)
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status":200,"reviews":reviews})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def get_dealer_details(request, dealer_id):
    """
    Fetches details of a specific dealer

    Args:
        dealer_id (int): The ID of the dealer

    Returns:
        JsonResponse: {"status": 200, "dealer": <dealer data>} if valid dealer_id,
                      {"status": 400, "message": "Bad Request"} otherwise
    """
    if(dealer_id):
        endpoint = "/fetchDealer/"+str(dealer_id)
        dealership = get_request(endpoint)
        return JsonResponse({"status":200,"dealer":dealership})
    else:
        return JsonResponse({"status":400,"message":"Bad Request"})

def add_review(request):
    """
    Submits a review for a dealer

    Requirements:
        - User must be authenticated (not anonymous)

    Request Body (JSON):
        - Review data fields as required by backend service

    Returns:
        JsonResponse: {"status": 200} if successful,
                      {"status": 401, "message": "Error in posting review"} on error,
                      {"status": 403, "message": "Unauthorized"} if user is not logged in
    """
    if(request.user.is_anonymous == False):
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status":200})
        except:
            return JsonResponse({"status":401,"message":"Error in posting review"})
    else:
        return JsonResponse({"status":403,"message":"Unauthorized"})

def get_inventory(request, dealer_id):
    """
    Fetches dealer inventory with optional filters

    Args:
        dealer_id (int): The ID of the dealer

    Query Parameters (optional):
        - year: Filter cars by year
        - make: Filter cars by make
        - model: Filter cars by model
        - mileage: Filter cars by max mileage
        - price: Filter cars by price

    Returns:
        JsonResponse: {"status": 200, "cars": <filtered inventory>} if successful,
                      {"status": 400, "message": "Bad Request"} otherwise
    """
    data = request.GET
    if (dealer_id):
        if 'year' in data:
            endpoint = "/carsbyyear/"+str(dealer_id)+"/"+data['year']
        elif 'make' in data:
            endpoint = "/carsbymake/"+str(dealer_id)+"/"+data['make']
        elif 'model' in data:
            endpoint = "/carsbymodel/"+str(dealer_id)+"/"+data['model']
        elif 'mileage' in data:
            endpoint = "/carsbymaxmileage/"+str(dealer_id)+"/"+data['mileage']
        elif 'price' in data:
            endpoint = "/carsbyprice/"+str(dealer_id)+"/"+data['price']
        else:
            endpoint = "/cars/"+str(dealer_id)
 
        cars = searchcars_request(endpoint)
        return JsonResponse({"status": 200, "cars": cars})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})
    return JsonResponse({"status": 400, "message": "Bad Request"})
