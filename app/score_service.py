from time import sleep

import boto3
from boto3.dynamodb.conditions import Key

from config import config
from dynamodb_admin import create_score_table

client = boto3.client(
    'dynamodb',
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key,
    region_name=config.region_name,
    endpoint_url=config.endpoint_url)
dynamodb = boto3.resource(
    'dynamodb',
    aws_access_key_id=config.aws_access_key_id,
    aws_secret_access_key=config.aws_secret_access_key,
    region_name=config.region_name,
    endpoint_url=config.endpoint_url)
existing_tables = client.list_tables()['TableNames']
if config.table_name not in existing_tables:
    create_score_table(dynamodb)

table = dynamodb.Table(config.table_name)


# When adding a global secondary index to an existing table, you cannot query the index until it has been backfilled.
# This portion of the script waits until the index is in the “ACTIVE” status, indicating it is ready to be queried.
def wait_until_active_index():
    while True:
        if not table.global_secondary_indexes or table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
            print('Waiting for index to backfill...')
            sleep(5)
            table.reload()
        else:
            break


def upsert_score(username, datetime, season, score):
    response = table.put_item(
        Item={
            'userID': username,
            'datetime': datetime,
            'season': season,
            'score': score
        }
    )
    return response


def query_score_for_user(username):
    response = table.query(
        KeyConditionExpression=Key('userID').eq(username)
    )
    items = response['Items']
    item_dic = {i: item for i, item in enumerate(items)}
    return item_dic


def get_highscores_for_current_season(limit=3):
    return get_highscores_for_season('1', limit)


def get_highscores_for_season(season, limit=3):
    wait_until_active_index()
    response = table.query(
        IndexName="HighScoreIndex",
        Limit=limit,
        KeyConditionExpression=Key('season').eq(season),
        ScanIndexForward=False
    )
    items = response['Items']
    item_dic = {i: item for i, item in enumerate(items)}
    return item_dic


def get_all_scores():
    response = table.scan()
    items = response['Items']
    item_dic = {i: item for i, item in enumerate(items)}
    return item_dic
