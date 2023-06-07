import os
import json
from db import DBTable


def get_key(event, context):
    try:
        provider_id = event["queryStringParameters"].get('provider')
        user_id = event["requestContext"]["authorizer"]["claims"]["sub"]
    except Exception as e:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Missing required parameters'
            })
        }

    if not provider_id:
        return {
            'statusCode': 400,
            'body': json.dumps({
                'message': 'Missing required parameters'
            })
        }

    keys_table = DBTable(os.getenv('KEYS_TABLE'))
    key = keys_table.get_sort('user_id', user_id, 'provider_id', provider_id)

    provider_id = key.get('provider_id')
    value = key.get('value')

    if provider_id and value:
        return {
            'statusCode': 200,
            'body': json.dumps({provider_id: value})
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({
                'message': 'Key not found'
            })
        }
