#!/bin/bash
docker-compose -f docker-compose.yml up

# docker-compose exec webserver airflow variables -i dags/config/trade_etanol_variables.json

# docker-compose exec webserver airflow connections -a \
# --conn_id 'trade-mysql'\
# --conn_type 'mysql'\
# --conn_host 'trade-mysql'\
# --conn_login 'root'\
# --conn_password 'root'\
# --conn_schema 'trade'