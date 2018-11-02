import json
import os

def get_restaurants(event, context):

    YELP_APP_KEY = os.getenv('YELP_APP_KEY', None)

    if YELP_APP_KEY is not None:
        return {
            "statusCode": 200,
            "body": {
                'error': True,
                'msg': 'Provide correct YELP_APP_KEY'
            }
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(event)
    }

    return response

    ***REMOVED*** Use this code if you don't use the http event with the LAMBDA-PROXY
    ***REMOVED*** integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
