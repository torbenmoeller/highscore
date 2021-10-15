import json


def create_score_table(dynamodb):
    table = dynamodb.create_table(
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


def delete_score_table(table):
    table.delete()


def load_scores(table):
    with open("scores_data.json") as json_file:
        scores = json.load(json_file)
    for score in scores:
        table.put_item(Item=score)
