from datetime import datetime

import uvicorn
from fastapi import FastAPI

from score_service import get_highscores_for_current_season, upsert_score, query_score_for_user, \
    get_all_scores

app = FastAPI()


@app.get("/scores")
def api_all_scores():
    return get_all_scores()


@app.get("/scores/{username}")
def api_get_score(username: str):
    return query_score_for_user(username)


@app.post("/scores/{username}")
@app.put("/scores/{username}")
def api_upsert_score(username: str, score: str):
    iso_time_now = datetime.now().isoformat()
    return upsert_score(username, iso_time_now, '1', score)


@app.get("/highscores")
def api_highscores(limit: int = 3):
    return get_highscores_for_current_season(int(limit))


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
