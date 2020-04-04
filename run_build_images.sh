#!/bin/bash
docker build -f "./AirflowDocker.Dockerfile" -t "airflow-docker" .

docker build -f "./MySqlDocker.Dockerfile" -t "mysql-docker" .

sh ./start_containers.sh