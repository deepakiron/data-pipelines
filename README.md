# data-pipelines
The repo hosts ETL data piplines codes to perform data operation on GCP environment


## Setup

### Setup file details
Repo contains 2 docker file 
1. airflow-docker-image 
   - contains the airflow image with all the requirements setup with it.
2. docker-compose.yml
   - compose file consist of Redis,Postgres,Airflow components.
   - refer [link](https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html) for more details


### Steps to follow to install in local environment   
1. Run `docker compose up` it will setup the airflow environment and expose into port `8080`.
2. open `localhost:8080` to open airflow webserver. the userid and password is `airflow`. if want to change it modify them in `docker-compose.yml` file

### Steps to follow to deploy it in GCP environment