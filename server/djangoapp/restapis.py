"""
API Client Utilities
--------------------
This file defines utility functions for interacting with external services 
and backend APIs. It loads environment variables for service URLs and provides 
helper functions for GET and POST requests.

Functions:
- get_request: Sends a GET request to the backend server 
- analyze_review_sentiments: Sends text to the sentiment analysis service and returns results
- post_review: Sends a POST request to the backend server to insert a new review
- searchcars_request: Sends a GET request to the car search service with optional query parameters
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# URL of the backend server
backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
# URL of the sentiment analysis service
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")
# URL of the car search service
searchcars_url = os.getenv(
    'searchcars_url',
    default="http://localhost:3050/")


def get_request(endpoint, **kwargs):
    """
    Sends a GET request to the backend server

    Args:
        endpoint (str): API endpoint to call 
        **kwargs: Optional query parameters as key-value pairs

    Returns:
        dict: JSON response from the backend if successful, and None otherwise
    """
    params = ""
    if(kwargs):
        for key,value in kwargs.items():
            params=params+key+"="+value+"&"

    request_url = backend_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        print("Network exception occurred")


def analyze_review_sentiments(text):
    """
    Sends a text string to the sentiment analysis service

    Args:
        text (str): Review text to analyze

    Returns:
        dict: Sentiment analysis results (JSON) if successful, and None otherwise
    """
    request_url = sentiment_analyzer_url+"analyze/"+text
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")


def post_review(data_dict):
    """
    Sends a review payload to the backend server via POST request

    Args:
        data_dict (dict): Dictionary containing review data

    Returns:
        dict: JSON response from the backend if successful, and None otherwise
    """
    request_url = backend_url+"/insert_review"
    try:
        response = requests.post(request_url,json=data_dict)
        print(response.json())
        return response.json()
    except:
        print("Network exception occurred")


def searchcars_request(endpoint, **kwargs):
    """
    Sends a GET request to the car search service

    Args:
        endpoint (str): API endpoint to call 
        **kwargs: Optional query parameters as key-value pairs

    Returns:
        dict: JSON response from the search service if successful, and None otherwise
    """
    params = ""
    if (kwargs):
        for key, value in kwargs.items():
            params = params+key + "=" + value + "&"

    request_url = searchcars_url+endpoint+"?"+params

    print("GET from {} ".format(request_url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except:
        print("Network exception occurred")
    finally:
        print("GET request call complete!")
        