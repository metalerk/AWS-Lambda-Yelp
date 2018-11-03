import asyncio
import json
import os
import requests as req
import urllib
import psycopg2

from psycopg2.extensions import AsIs


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
    restaurants = response.json()['businesses']

    if restaurants.__len__() > 0:
        return [{
            'id': x['id'],
            'name': x['name'],
            'rating': x['rating'],
            'latitude': x['coordinates']['latitude'],
            'longitude': x['coordinates']['longitude'],
            'phone': x['phone'],

        } for x in restaurants]

    return restaurants


def write_json_to_db(obj, table):
    connect_str = "host={} dbname={} user={} password={}".format(
        os.getenv('DB_HOST', ''),
        os.getenv('DB_NAME', ''),
        os.getenv('DB_USER', ''),
        os.getenv('DB_PASSWD', ''),
    )
    conn = psycopg2.connect(connect_str)
    conn.autocommit = True
    cursor = conn.cursor()

    sql_statement = """
INSERT INTO {table} (yelp_id, name, rating, latitude, longitude, phone)
VALUES ('{yelp_id}', '{name}', {rating}, {latitude}, {longitude}, '{phone}');
    """

    for item in obj:
        cursor.execute(sql_statement.format(
            table=AsIs(table),
            yelp_id=item['id'],
            name=item['name'],
            rating=item['rating'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            phone=item['phone']
        ))
    conn.close()


def main(event, context):

    if YELP_APP_KEY is None:
        return {
            'statusCode': 200,
            'body': {
                'error': {
                    'code': 'YELP_KEY_MISSING',
                    'description': 'Provide correct YELP_APP_KEY',
                }
            }
        }

    restaurants = get_restaurants(**event)
    write_json_to_db(obj=restaurants, table=os.getenv('RESTAURANTS', None))

    response = {
        'statusCode': 200,
        'body': {
            'restaurants': restaurants,
        }
    }

    return response
