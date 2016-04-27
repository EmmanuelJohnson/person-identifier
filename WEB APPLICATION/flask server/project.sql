-- phpMyAdmin SQL Dump
-- version 4.0.10deb1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 01, 2016 at 01:43 AM
-- Server version: 5.5.47-0ubuntu0.14.04.1
-- PHP Version: 5.5.9-1ubuntu4.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `project`
--

-- --------------------------------------------------------

--
-- Table structure for table `companies`
--

CREATE TABLE IF NOT EXISTS `companies` (
  `cid` int(10) NOT NULL AUTO_INCREMENT,
  `companyname` varchar(100) NOT NULL,
  PRIMARY KEY (`cid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=2 ;

--
-- Dumping data for table `companies`
--

INSERT INTO `companies` (`cid`, `companyname`) VALUES
(1, 'Bobs Rasp');

-- --------------------------------------------------------

--
-- Table structure for table `info`
--

CREATE TABLE IF NOT EXISTS `info` (
  `infoid` int(11) NOT NULL AUTO_INCREMENT,
  `uid` int(20) NOT NULL,
  `fname` text NOT NULL,
  `age` int(11) NOT NULL,
  `gender` text NOT NULL,
  `relationship` text NOT NULL,
  `otherinfo` text NOT NULL,
  `companyid` int(11) NOT NULL,
  PRIMARY KEY (`infoid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `info`
--

INSERT INTO `info` (`infoid`, `uid`, `fname`, `age`, `gender`, `relationship`, `otherinfo`, `companyid`) VALUES
(4, 5, 'bobby', 21, 'Male', 'Cousin', 'Best cousin', 0);

-- --------------------------------------------------------

--
-- Table structure for table `invitations`
--

CREATE TABLE IF NOT EXISTS `invitations` (
  `iid` int(10) NOT NULL AUTO_INCREMENT,
  `recid` int(10) NOT NULL,
  `companyid` int(10) NOT NULL,
  `canid` int(10) NOT NULL,
  `status` int(2) NOT NULL,
  `nickemail` varchar(60) NOT NULL,
  PRIMARY KEY (`iid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=7 ;

--
-- Dumping data for table `invitations`
--

INSERT INTO `invitations` (`iid`, `recid`, `companyid`, `canid`, `status`, `nickemail`) VALUES
(6, 1, 1, 5, 2, 'bobbyda.16@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(10) NOT NULL AUTO_INCREMENT,
  `email` varchar(90) NOT NULL,
  `password` varchar(30) NOT NULL,
  `name` varchar(90) NOT NULL,
  `type` int(2) NOT NULL,
  `companyid` int(5) NOT NULL,
  `status` int(2) NOT NULL,
  `imageurl` varchar(500) NOT NULL,
  PRIMARY KEY (`uid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=6 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `email`, `password`, `name`, `type`, `companyid`, `status`, `imageurl`) VALUES
(1, 'bobims.16@gmail.com', 'bobbyda', 'Bobby', 1, 1, 2, ''),
(5, 'bobbyda.16@gmail.com', '', 'bobbyda', 2, 0, 2, 'https://lh4.googleusercontent.com/-Vi4tDvJvyuM/AAAAAAAAAAI/AAAAAAAAABM/kZYCUQ50sy8/s96-c/photo.jpg');

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
