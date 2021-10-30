from pprint import pprint
from random import randrange, seed

import boto3
from starlette.testclient import TestClient

from app.dynamodb_admin import create_score_table, delete_score_table, load_scores

from app.main import app

dynamodb_client = boto3.client('dynamodb', endpoint_url="http://127.0.0.1:8000")
dynamodb = boto3.resource('dynamodb', endpoint_url="http://127.0.0.1:8000")
client = TestClient(app)
base_url = "http://127.0.0.1:5000"
# base_url = "http://192.168.178.13:32144"
scores_path = "/scores"
highscores_path = "/highscores"
limit = "?limit=5"


def add_user_data(username, count=5):
    url = base_url + scores_path + username
    for x in range(3):
        score = randrange(10000)
        print(score)
        client.put(url, data=str(score))
    # r = requests.get(url)
    # pprint(r.json())


if __name__ == "__main__":
    existing_tables = dynamodb_client.list_tables()['TableNames']
    if 'Scores' in existing_tables:
        table = dynamodb.Table('Scores')
        delete_score_table(table)
    table = create_score_table(dynamodb)
    load_scores(table)

    seed(1234)

    # Check imported data
    response = client.get("/scores")
    assert response.status_code == 200

    # Add new user
    add_user_data("/user4", 3)

    # Check user4 data
    response = client.get("/scores")
    assert response.status_code == 200

    url = base_url + highscores_path
    r = client.get(url)
    assert response.status_code == 200
    pprint(r.json())

    url = base_url + highscores_path + limit
    r = client.get(url)
    assert response.status_code == 200
    pprint(r.json())

    url = base_url + scores_path
    r = client.get(url)
    assert response.status_code == 200
    pprint(r.json())
