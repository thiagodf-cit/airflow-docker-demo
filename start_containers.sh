#!/bin/bash

# Start MySql
# docker run -d -p 3306:3306 --name trade-mysql \
# -e MYSQL_ROOT_PASSWORD=root \
# -e MYSQL_DATABASE=trade \
# mysql

# docker exec -it trade-mysql bash
# mysql -uroot -p
# MySql@2020!
# show databases;
# use trade;
# show tables;
# CREATE TABLE etanol_anidro (ref_date varchar (50) NOT NULL, value_per_liter_brl varchar (50) NOT NULL, value_per_liter_usd varchar (50) NOT NULL, weekly_variation varchar (50) NOT NULL);
# show tables;
# show columns from etanol_anidro;
# INSERT INTO etanol_anidro (ref_date, value_per_liter_brl, value_per_liter_usd, weekly_variation) VALUES ('20/03/2020', '2.02', '0.3979', '-6.20');
# show columns from etanol_anidro;
# SELECT COUNT(*) FROM etanol_anidro;


docker-compose -f docker-compose.yml up --abort-on-container-exit