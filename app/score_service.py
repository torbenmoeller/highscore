from time import sleep

import boto3
from boto3.dynamodb.conditions import Key

from config import config
from dynamodb_admin import create_score_table


class ScoringService:
    def __init__(self):
        self.client = boto3.client(
            'dynamodb',
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            region_name=config.region_name,
            endpoint_url=config.endpoint_url)
        self.dynamodb = boto3.resource(
            'dynamodb',
            aws_access_key_id=config.aws_access_key_id,
            aws_secret_access_key=config.aws_secret_access_key,
            region_name=config.region_name,
            endpoint_url=config.endpoint_url)
        existing_tables = self.client.list_tables()['TableNames']
        if config.table_name not in existing_tables:
            create_score_table(self.dynamodb)
        self.table = self.dynamodb.Table(config.table_name)

    # When adding a global secondary index to an existing table,
    # you cannot query the index until it has been backfilled.
    # This portion of the script waits until the index is in the “ACTIVE” status, indicating it is ready to be queried.
    def wait_until_active_index(self):
        while True:
            if not self.table.global_secondary_indexes or \
                    self.table.global_secondary_indexes[0]['IndexStatus'] != 'ACTIVE':
                print('Waiting for index to backfill...')
                sleep(5)
                self.table.reload()
            else:
                break

    def upsert_score(self, username, datetime, season, score):
        response = self.table.put_item(
            Item={
                'userID': username,
                'datetime': datetime,
                'season': season,
                'score': score
            }
        )
        return response

    def query_score_for_user(self, username):
        response = self.table.query(
            KeyConditionExpression=Key('userID').eq(username)
        )
        items = response['Items']
        item_dic = {i: item for i, item in enumerate(items)}
        return item_dic

    def get_highscores_for_current_season(self, limit=3):
        return self.get_highscores_for_season('1', limit)

    def get_highscores_for_season(self, season, limit=3):
        self.wait_until_active_index()
        response = self.table.query(
            IndexName="HighScoreIndex",
            Limit=limit,
            KeyConditionExpression=Key('season').eq(season),
            ScanIndexForward=False
        )
        items = response['Items']
        item_dic = {i: item for i, item in enumerate(items)}
        return item_dic

    def get_all_scores(self):
        response = self.table.scan()
        items = response['Items']
        item_dic = {i: item for i, item in enumerate(items)}
        return item_dic

    def table_exists(self):
        try:
            self.client.describe_table(TableName=config.table_name)
        except self.client.exceptions.ResourceNotFoundException as ex:
            print(ex)
            return False
        return True



