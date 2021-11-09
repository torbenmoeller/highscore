from time import sleep

from boto3.dynamodb.conditions import Key

from config import config
from dynamodb_client import dynamodb_client
from dynamodb_resource import dynamodb_resource


def table_exists():
    try:
        dynamodb_client.describe_table(TableName=config.table_name)
    except dynamodb_client.exceptions.ResourceNotFoundException as ex:
        print(ex)
        return False
    return True


def create():
    table = dynamodb_resource.create_table(
        TableName='Scores',
        KeySchema=[
            {
                'AttributeName': 'userID',
                'KeyType': 'HASH',
            },
            {
                'AttributeName': 'datetime',
                'KeyType': 'RANGE'
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userID',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'datetime',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'season',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'score',
                'AttributeType': 'S'
            }
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        },
        GlobalSecondaryIndexes=[
            {
                "IndexName": "HighScoreIndex",
                "KeySchema": [
                    {
                        "AttributeName": "season",
                        "KeyType": "HASH"
                    },
                    {
                        'AttributeName': 'score',
                        'KeyType': 'RANGE'
                    }
                ],
                "Projection": {
                    "ProjectionType": "ALL"
                },
                "ProvisionedThroughput": {
                    "ReadCapacityUnits": 1,
                    "WriteCapacityUnits": 1,
                }
            }
        ]
    )
    return table


class ScoresTable:
    def __init__(self):
        if not table_exists():
            create()
        self.table = dynamodb_resource.Table(config.table_name)

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

    def upsert_scores(self, scores):
        for score in scores:
            self.table.put_item(Item=score)

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

    def delete(self):
        self.table.delete()


scores_table = ScoresTable()
