import json


def hello(event, context):
    response = {
        "statusCode": 200,
        'headers': {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": True

        },
        "body": "Hello, World!"
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def authentication(event, context):
    request_payload = json.loads(event['body'])
    username = request_payload['username']
    password = request_payload['password']

    if 'user' not in request_payload['username']:
        return {
            'statusCode': 404,
            'body': 'User not found'
        }
    body = {'token': f'token.{username}.{password}'}
    return {
        'statusCode': 200,
        'body': json.dumps(body)
    }


def authorization(event, context):
    print(f'Event[{type(event)}] ' + str(event))
    print('########################################')
    print(f'Header Type[{type(event["headers"])}] ' + str(event["headers"]))
    token = event['headers'] \
        .get('Authorization', 'Bearer ') \
        .replace('Bearer ', '')

    if 'token' not in token:
        return {
            'statusCode': 403,
            'body': 'You are forbidden'
        }

    return {
        'statusCode': 200,
        'body': 'User is allowed to do this operation'
    }
