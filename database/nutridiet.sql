-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Mar 15, 2023 at 08:28 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 7.3.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nutridiet`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `Admin id` int(10) NOT NULL,
  `email` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `contact`
--

CREATE TABLE `contact` (
  `id` int(11) DEFAULT NULL,
  `sno` int(50) NOT NULL,
  `name` text NOT NULL,
  `email` varchar(50) NOT NULL,
  `phone_num` varchar(15) NOT NULL,
  `msg` text NOT NULL,
  `date` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contact`
--

INSERT INTO `contact` (`id`, `sno`, `name`, `email`, `phone_num`, `msg`, `date`) VALUES
(NULL, 1, 'Fatima', 'fatima22@gmail.com', '0432146536', 'hey', '2023-01-08 00:00:00'),
(NULL, 20, 'fatima masood', 'bsef19m020@gmail.com', '03435762672', 'i wana generate diet plan', NULL),
(NULL, 21, 'fatima', 'fatima22@gmail.com', '0432657432', 'hey i wana generate a diet plan', NULL),
(NULL, 22, 'NutriDiet', 'saba@gmail.com', '098787575', 'njf', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `dietplan`
--

CREATE TABLE `dietplan` (
  `planid` int(11) NOT NULL,
  `id` int(11) NOT NULL,
  `fooditems` text NOT NULL,
  `quantity` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `query`
--

CREATE TABLE `query` (
  `queryid` int(11) NOT NULL,
  `query` varchar(100) NOT NULL,
  `id` int(11) NOT NULL,
  `Admin id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`id`, `name`, `username`, `password`) VALUES
(1, '', '', ''),
(2, 'fatima123', 'fatima123', 'fatima123@gmail.com'),
(3, 'usama12', 'usama1122@gmail.com', 'usama123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`Admin id`);

--
-- Indexes for table `contact`
--
ALTER TABLE `contact`
  ADD PRIMARY KEY (`sno`),
  ADD UNIQUE KEY `id` (`id`);

--
-- Indexes for table `dietplan`
--
ALTER TABLE `dietplan`
  ADD PRIMARY KEY (`planid`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `query`
--
ALTER TABLE `query`
  ADD PRIMARY KEY (`queryid`),
  ADD KEY `id` (`id`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `contact`
--
ALTER TABLE `contact`
  MODIFY `sno` int(50) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `dietplan`
--
ALTER TABLE `dietplan`
  MODIFY `planid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `query`
--
ALTER TABLE `query`
  MODIFY `queryid` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `user`
--
ALTER TABLE `user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `dietplan`
--
ALTER TABLE `dietplan`
  ADD CONSTRAINT `dietplan_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`);

--
-- Constraints for table `query`
--
ALTER TABLE `query`
  ADD CONSTRAINT `query_ibfk_1` FOREIGN KEY (`id`) REFERENCES `user` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
