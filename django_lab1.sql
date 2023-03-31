-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 31, 2023 at 11:39 PM
-- Server version: 8.0.24
-- PHP Version: 8.0.8

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `django_lab1`
--

-- --------------------------------------------------------

--
-- Table structure for table `dishes`
--

CREATE TABLE `dishes` (
  `id` int NOT NULL,
  `name` varchar(64) COLLATE utf8mb4_general_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dishes`
--

INSERT INTO `dishes` (`id`, `name`) VALUES
(1, 'Паста з куркою та грибами'),
(2, 'Картопля з м\'ясом'),
(3, 'Плов з овочами'),
(6, 'Рис з куркою'),
(7, 'Gavno');

-- --------------------------------------------------------

--
-- Table structure for table `dish_ingredients`
--

CREATE TABLE `dish_ingredients` (
  `id` int NOT NULL,
  `dish_id` int NOT NULL,
  `ingredient_id` int NOT NULL,
  `count` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `dish_ingredients`
--

INSERT INTO `dish_ingredients` (`id`, `dish_id`, `ingredient_id`, `count`) VALUES
(18, 6, 3, 200),
(19, 6, 6, 200),
(20, 1, 4, 200),
(21, 1, 3, 200),
(22, 1, 2, 200),
(23, 1, 1, 200),
(24, 2, 7, 200),
(25, 2, 9, 200),
(26, 2, 5, 200),
(27, 3, 11, 200),
(28, 3, 9, 200),
(29, 3, 8, 200),
(30, 3, 2, 200),
(31, 3, 6, 200),
(32, 7, 4, 200),
(33, 7, 3, 200),
(34, 7, 8, 200),
(35, 7, 5, 200);

-- --------------------------------------------------------

--
-- Table structure for table `ingredients`
--

CREATE TABLE `ingredients` (
  `id` int NOT NULL,
  `name` varchar(64) COLLATE utf8mb4_general_ci NOT NULL,
  `price` float NOT NULL,
  `count` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `ingredients`
--

INSERT INTO `ingredients` (`id`, `name`, `price`, `count`) VALUES
(1, 'Спагетті', 40, 11550),
(2, 'Помідор', 96, 2200),
(3, 'Куряче філе', 140, 4600),
(4, 'Гриби печериці', 109, 1900),
(5, 'Сир твердий', 300, 900),
(6, 'Рис', 60, 3850),
(7, 'Картопля', 20, 29750),
(8, 'Морква', 20, 9900),
(9, 'М\'ясо свинини', 210, 2400),
(10, 'Куряче яйце', 100, 6000),
(11, 'Ізюм', 150, 1250);

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int NOT NULL,
  `name` varchar(1024) COLLATE utf8mb4_general_ci NOT NULL,
  `sum` float NOT NULL,
  `order_datetime` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `name`, `sum`, `order_datetime`) VALUES
(1, 'Паста з куркою та грибами', 260, '2023-02-15 22:52:27'),
(2, 'Паста з куркою та грибами', 260, '2023-03-22 19:18:16'),
(3, 'Стейк зі свинини з картопляним пюре, Плов з м\'ясом та овочами', 289, '2023-03-30 23:28:05'),
(4, 'Паста з куркою та грибами', 130, '2023-03-30 23:28:35');

-- --------------------------------------------------------

--
-- Table structure for table `order_dishes`
--

CREATE TABLE `order_dishes` (
  `id` int NOT NULL,
  `order_id` int NOT NULL,
  `dish_id` int NOT NULL,
  `count` int NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_dishes`
--

INSERT INTO `order_dishes` (`id`, `order_id`, `dish_id`, `count`) VALUES
(1, 1, 1, 2),
(2, 2, 1, 2),
(3, 3, 2, 1),
(4, 3, 3, 1),
(5, 4, 1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `dishes`
--
ALTER TABLE `dishes`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_di_dish_id` (`dish_id`),
  ADD KEY `fk_di_ingradient_id` (`ingredient_id`);

--
-- Indexes for table `ingredients`
--
ALTER TABLE `ingredients`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_dishes`
--
ALTER TABLE `order_dishes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `fk_od_dish_id` (`dish_id`),
  ADD KEY `fk_od_ingradient_id` (`order_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `dishes`
--
ALTER TABLE `dishes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- AUTO_INCREMENT for table `ingredients`
--
ALTER TABLE `ingredients`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `order_dishes`
--
ALTER TABLE `order_dishes`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dish_ingredients`
--
ALTER TABLE `dish_ingredients`
  ADD CONSTRAINT `fk_di_dish_id` FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`),
  ADD CONSTRAINT `fk_di_ingradient_id` FOREIGN KEY (`ingredient_id`) REFERENCES `ingredients` (`id`);

--
-- Constraints for table `order_dishes`
--
ALTER TABLE `order_dishes`
  ADD CONSTRAINT `fk_od_dish_id` FOREIGN KEY (`dish_id`) REFERENCES `dishes` (`id`),
  ADD CONSTRAINT `fk_od_ingradient_id` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
