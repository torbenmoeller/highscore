#Highscore

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li><a href="#technologies">Technologies</a></li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#issues">Issues</a></li>
    <li><a href="#toDo">ToDo</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## About the Project
Highscore is a containerized python service for 
* Storing scores of users
* Getting highest scores of a user
* Getting highest overall scores
* Getting all scores 

The service offers a REST interface and stores the data in DynamoDB. 

GitHub Actions are used to push the container to  
[Docker Hub](https://hub.docker.com/repository/docker/torben/highscore).


## Technologies
* Local development
  * Python
  * FastApi
  * Local DynamoDB Container
  * Docker
  * Docker Compose
* Cloud
  * Terraform Cloud
  * AWS EKS
  * Kubernetes
* Test
  * Postman
* CI/CD
  * GitHub Actions
  * CodeQL
  * Sonar
  * Dependabot
  * Docker Hub

# Usage
Docker compose can build and run every container locally. 
You can make a health check with curl.
```bash
docker compose up -d --build
curl --location --request GET 'http://127.0.0.1:5000/health'
```

# Issues
* Scores are sorted lexically (Actually very critical 🙈)

# ToDo
* Create complete AWS environment with terraform cloud
  * IAM / Security groups
  * Use Terraform output for configuration
* Deploy to EKS
* Remove Dynamodb-container from EKS deployment
* Unit tests
* Run Postman in GitHub Action with Newman
* Fill generated OpenApi with description and default values
* Authentication
* Opensource Licenses

* Snyk scan for container security
* Add GitHub security policy

* Maybe
  * Add volumes to K8s dynamodb
  * Monitoring
  * Observability
  * Deploy as a Function


# License
The code distributed under the MIT license. See LICENSE for more information.

# Contact
Get in touch: contact@pluvial.dev