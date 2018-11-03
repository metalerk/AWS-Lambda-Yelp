import asyncio
import json
import os
import requests as req
import urllib


YELP_APP_KEY = os.getenv('YELP_APP_KEY', None)
YELP_API_ENDPOINT = 'https://api.yelp.com/v3'
HEADERS = {'Authorization': 'Bearer {}'.format(YELP_APP_KEY)}


def get_restaurants(search_term, latitude, longitude, radius=0):
    PARAMS = {
        'term': search_term,
        'latitude': latitude,
        'longitude': longitude,
        'radius': radius,
    }
    endpoint = '{}/businesses/search'.format(YELP_API_ENDPOINT)
    response = req.get(
        endpoint,
        headers=HEADERS,
        params=PARAMS
    )

    return response

def main(event, context):

    if YELP_APP_KEY is None:
        return {
            "statusCode": 200,
            "body": {
                'error': {
                    'code': 'YELP_KEY_MISSING',
                    'description': 'Provide correct YELP_APP_KEY',
                }
            }
        }

    restaurants = get_restaurants(**event)
    response = {
        "statusCode": 200,
        "body": restaurants.json()
    }

    return response
