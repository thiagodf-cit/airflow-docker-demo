CREATE DATABASE trade

DROP TABLE IF EXISTS trade.etanol_anidro

CREATE TABLE trade.etanol_anidro (ref_date varchar (50) NOT NULL, value_per_liter_brl varchar (50) NOT NULL, value_per_liter_usd varchar (50) NOT NULL, weekly_variation varchar (50) NOT NULL);

SELECT COUNT(*) FROM trade.etanol_anidro;

SELECT * FROM trade.etanol_anidro

DELETE FROM trade.etanol_anidro

INSERT INTO trade.etanol_anidro (ref_date, value_per_liter_brl, value_per_liter_usd, weekly_variation) VALUES ('20/03/2020', '2.02', '0.3979', '-6.20');