# Highscore

# Features
* Stores score of users
* Shows highest scores of a user
* Shows highest overall scores
* Shows all scores

# Used technologies
* Python
* FastApi
* DynamoDb
* Local development with Docker Compose
* Deployment on Kubernetes
* Tests with Postman
* Dependabot

# Installation
pip install -r requirements.txt

docker build --tag highscore:latest .

# Quickstart
docker compose up -d --build

docker compose down

# Kubernetes
kubectl apply -f k8s-deployment.yml -n highscore

# Issues
* Scores are sorted lexically

# ToDo
* Automate build with Github Actions
* Publish container
* Setup AWS environment with terraform
* Deploy to EKS
* Unit tests
* Run Postman in Github Action with Newman
* Authentication
* Fill this ReadMe
* Opensource Licenses
* Add volumes to K8s dynamodb

* Snyk scan for container security
* Python code scan with Sonar

* Maybe monitoring
* Maybe observability
* Maybe deploy as a Function
