import asyncio
import json
import os
import requests as req
import urllib
import psycopg2


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

    return response.json()


def write_json_to_db(obj, table):
    connect_str = "host={} dbname={} user={} password={}".format(
        os.getenv('DB_HOST', ''),
        os.getenv('DB_NAME', ''),
        os.getenv('DB_USER', ''),
        os.getenv('DB_PASSWD', ''),
    )
    conn = psycopg2.connect(connect_str)
    cursor = conn.cursor()

    sql_statement = """
INSERT INTO {table}
SELECT *
FROM   json_populate_recordset(null::{table},
          json json.dumps({obj}));
    """.format(table=table, obj=obj)

    cursor.execute()
    conn.close()


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
    if restaurants['businesses'].__len__():
        write_to_db(items=restaurants, json=True)

    response = {
        "statusCode": 200,
        "body": restaurants,
    }

    return response
