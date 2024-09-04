-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-09-04 03:14:33
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
-- 資料表結構 `water_external_measure_station`
--

CREATE TABLE `water_external_measure_station` (
  `id` varchar(50) NOT NULL COMMENT '測站代號',
  `type` varchar(50) DEFAULT NULL COMMENT '站點類型(River:河川 ； Rainy: 雨量站)',
  `name` varchar(50) NOT NULL COMMENT '測站名稱',
  `longitude` decimal(9,6) NOT NULL COMMENT '經度',
  `latitude` decimal(8,6) NOT NULL COMMENT '緯度',
  `created_at` datetime NOT NULL DEFAULT current_timestamp() COMMENT '創建時間',
  `updated_at` datetime NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp() COMMENT '修改時間'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `water_external_measure_station`
--
ALTER TABLE `water_external_measure_station`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
