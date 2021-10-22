# syntax=docker/dockerfile:1

FROM python:3.8.0-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r requirements.txt
COPY ./app ./app
CMD [ "uvicorn", "app.main:app" , "--host", "0.0.0.0", "--port", "5000"]
