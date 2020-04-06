import json
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def hello(_, __):
    response = {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True

        },
        'body': 'Hello, World!'
    }
    return response


def authentication(event, _):
    logger.info(f"#### Event[{type(event['body'])} ####")
    logger.info(event)
    request_payload = json.loads(event['body'])
    username = request_payload['username']
    password = request_payload['password']

    body = {'token': f'token.{username}.{password}'}
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True

        },
        'body': json.dumps(body)
    }


def authorization(event, _):
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
