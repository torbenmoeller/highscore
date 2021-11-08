from datetime import datetime

import uvicorn
from fastapi import FastAPI, HTTPException

from config import config
from score_service import ScoringService

app = FastAPI()
scoring_service = ScoringService()


@app.get("/scores")
def api_all_scores():
    return scoring_service.get_all_scores()


@app.get("/scores/{username}")
def api_get_score(username: str):
    return scoring_service.query_score_for_user(username)


@app.post("/scores/{username}")
@app.put("/scores/{username}")
def api_upsert_score(username: str, score: str):
    iso_time_now = datetime.now().isoformat()
    return scoring_service.upsert_score(username, iso_time_now, '1', score)


@app.get("/highscores")
def api_highscores(limit: int = 3):
    return scoring_service.get_highscores_for_current_season(int(limit))


@app.get("/health")
def api_health():
    if config.aws_access_key_id is None:
        raise HTTPException(status_code=500, detail="AWS Access Key not set")
    if config.aws_secret_access_key is None:
        raise HTTPException(status_code=500, detail="AWS Secret Key not set")
    if config is None:
        raise HTTPException(status_code=500, detail="Config file not found")
    if not scoring_service.table_exists():
        raise HTTPException(status_code=500, detail="Error while describing table")
    result = {
        'aws_access_key_id': config.aws_access_key_id,
        'aws_secret_access_key': '***',
        'region_name': config.region_name,
        'endpoint_url': config.endpoint_url,
        'table_name': config.table_name
    }
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
