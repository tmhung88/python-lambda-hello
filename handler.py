import json
import logging
import boto3
import os
logger = logging.getLogger()
logger.setLevel(logging.INFO)

pool_id = os.environ.get('USER_POOL_ID')
client_id = os.environ.get('USER_POOL_CLIENT_ID')

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


    client = boto3.client('cognito-idp')
    auth_response = client.initiate_auth(
        ClientId=client_id,
        AuthFlow='USER_PASSWORD_AUTH',
        AuthParameters={
            'USERNAME': username,
            'PASSWORD': password
        }
    )
    logger.info(f'#### Authentication[{type(auth_response)}] #####')
    logger.info(auth_response)
    auth_result = auth_response['AuthenticationResult']
    body = {
        'token': auth_result['IdToken'],
        'expired_in': auth_result['ExpiresIn'],
        'token_type': auth_result['TokenType']
    }
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
