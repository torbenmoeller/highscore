import json
from pprint import pprint
from random import randrange, seed

import requests

from app.scores import scores_table, table_exists, create

base_url = "http://127.0.0.1:5000"
scores_path = "/scores"
highscores_path = "/highscores"
limit = "?limit=5"


def add_user_data(username, count=5):
    url = base_url + scores_path + username
    for x in range(3):
        score = randrange(10000)
        print(score)
        requests.put(url, data=str(score))


if __name__ == "__main__":
    if table_exists():
        scores_table.delete()
    create()

    table = scores_table

    with open("../test/scores_data.json") as json_file:
        scores = json.load(json_file)
    scores_table.upsert_scores(table, scores)

    seed(1234)

    # Check imported data
    response = requests.get("/scores")
    assert response.status_code == 200

    # Add new user
    add_user_data("/user4", 3)

    # Check user4 data
    response = requests.get("/scores")
    assert response.status_code == 200

    url = base_url + highscores_path
    r = requests.get(url)
    assert response.status_code == 200
    pprint(r.json())

    url = base_url + highscores_path + limit
    r = requests.get(url)
    assert response.status_code == 200
    pprint(r.json())

    url = base_url + scores_path
    r = requests.get(url)
    assert response.status_code == 200
    pprint(r.json())
