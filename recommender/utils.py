from urllib.parse import quote
from urllib.parse import urlencode


import os
import argparse
import json
import sys
import requests
from ceat.settings import BASE_DIR

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
TOKEN_PATH = '/oauth2/token'
GRANT_TYPE = 'client_credentials'


with open(os.path.join(BASE_DIR, 'yelpkeys.txt')) as f:
    CLIENT_ID, CLIENT_SECRET = f.read().splitlines()


def obtain_bearer_token(host, path):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        str: OAuth bearer token, obtained using client_id and client_secret.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    assert CLIENT_ID, "Please supply your client_id."
    assert CLIENT_SECRET, "Please supply your client_secret."
    data = urlencode({
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': GRANT_TYPE,
    })
    headers = {
        'content-type': 'application/x-www-form-urlencoded',
    }
    response = requests.request('POST', url, data=data, headers=headers)
    bearer_token = response.json()['access_token']
    return bearer_token

def request(host, path, bearer_token, url_params=None):
    """Given a bearer token, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        bearer_token (str): OAuth bearer token, obtained using client_id and client_secret.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % bearer_token,
    }

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()

def search(bearer_token, longitude, latitude, term, categories):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        longitude (double): The search longitude passed to the API.
        latitude (double): The search latitude passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'longitude': longitude,
        'latitude': latitude,
        'categories': categories,
        'limit': 50,
        'radius': 40000
    }

    if term:
        url_params['term'] = term.replace(' ', '+')

    return request(API_HOST, SEARCH_PATH, bearer_token, url_params=url_params)


def query_api(longitude, latitude, term=None, categories='restaurants'):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        longitude (double): The search longitude of the query.
        latitude (double): The search latitude of the query.
    """
    bearer_token = obtain_bearer_token(API_HOST, TOKEN_PATH)

    response = search(bearer_token, longitude, latitude, term, categories)
    return response
