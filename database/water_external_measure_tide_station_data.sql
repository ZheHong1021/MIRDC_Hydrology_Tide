-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-09-04 03:14:14
-- 伺服器版本： 10.4.24-MariaDB
-- PHP 版本： 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `feedsystem`
--

-- --------------------------------------------------------

--
-- 資料表結構 `water_external_measure_tide_station_data`
--

CREATE TABLE `water_external_measure_tide_station_data` (
  `id` int(11) NOT NULL,
  `level` float DEFAULT NULL COMMENT '潮高(單位:mm)',
  `measure_time` datetime NOT NULL COMMENT '測量時間',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '創建時間',
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '修改時間',
  `station_id` varchar(50) NOT NULL COMMENT '測站代號'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `water_external_measure_tide_station_data`
--
ALTER TABLE `water_external_measure_tide_station_data`
  ADD PRIMARY KEY (`id`),
  ADD KEY `index_measure_time_station_id_external_data` (`measure_time`,`station_id`),
  ADD KEY `FK_water_external_measure_tide_level_station_id` (`station_id`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `water_external_measure_tide_station_data`
--
ALTER TABLE `water_external_measure_tide_station_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `water_external_measure_tide_station_data`
--
ALTER TABLE `water_external_measure_tide_station_data`
  ADD CONSTRAINT `FK_water_external_measure_tide_level_station_id` FOREIGN KEY (`station_id`) REFERENCES `water_external_measure_station` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
