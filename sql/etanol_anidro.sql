-- Adminer 4.7.6 MySQL dump

SET NAMES utf8;
SET time_zone = '+00:00';
SET foreign_key_checks = 0;
SET sql_mode = 'NO_AUTO_VALUE_ON_ZERO';

SET NAMES utf8mb4;

DROP DATABASE IF EXISTS `trade`;
CREATE DATABASE `trade` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `trade`;

DROP TABLE IF EXISTS `etanol_anidro`;
CREATE TABLE `etanol_anidro` (
  `ref_date` varchar(50) NOT NULL,
  `value_per_liter_brl` varchar(50) NOT NULL,
  `value_per_liter_usd` varchar(50) NOT NULL,
  `weekly_variation` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

INSERT INTO `etanol_anidro` (`ref_date`, `value_per_liter_brl`, `value_per_liter_usd`, `weekly_variation`) VALUES
('20/03/2020',	'2.02',	'0.3979',	'-6.20')
ON DUPLICATE KEY UPDATE `ref_date` = VALUES(`ref_date`), `value_per_liter_brl` = VALUES(`value_per_liter_brl`), `value_per_liter_usd` = VALUES(`value_per_liter_usd`), `weekly_variation` = VALUES(`weekly_variation`);

-- 2020-04-03 15:24:39
