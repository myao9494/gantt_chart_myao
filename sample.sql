-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.22-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- gantt_howto_node のデータベース構造をダンプしています
CREATE DATABASE IF NOT EXISTS `gantt_howto_node` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `gantt_howto_node`;

--  テーブル gantt_howto_node.gantt_links の構造をダンプしています
CREATE TABLE IF NOT EXISTS `gantt_links` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` int(11) DEFAULT NULL,
  `target` int(11) DEFAULT NULL,
  `type` varchar(1) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- エクスポートするデータが選択されていません

--  テーブル gantt_howto_node.gantt_tasks の構造をダンプしています
CREATE TABLE IF NOT EXISTS `gantt_tasks` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `text` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `start_date` datetime DEFAULT NULL,
  `end_date` datetime DEFAULT NULL,
  `duration` int(11) NOT NULL DEFAULT 1,
  `progress` float NOT NULL DEFAULT 0,
  `parent` int(11) DEFAULT NULL,
  `kind_task` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `ToDo` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `task_schedule` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `folder` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `url_adress` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `mail` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `memo` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `hyperlink` text COLLATE utf8_unicode_ci DEFAULT NULL,
  `color` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `textColor` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `owner_id` int(11) DEFAULT NULL,
  `sortorder` int(11) DEFAULT NULL,
  `edit_date` text COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;