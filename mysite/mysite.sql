-- phpMyAdmin SQL Dump
-- version 3.4.10.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 20, 2013 at 09:28 PM
-- Server version: 5.5.21
-- PHP Version: 5.3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `mysite`
--

-- --------------------------------------------------------

--
-- Table structure for table `courses`
--

CREATE TABLE IF NOT EXISTS `courses` (
  `cid` int(30) NOT NULL AUTO_INCREMENT,
  `cname` varchar(50) NOT NULL,
  `owner` varchar(30) NOT NULL,
  `start_date` date NOT NULL,
  `no_of_followers` int(30) DEFAULT '0',
  `category` varchar(50) NOT NULL,
  `rating` float DEFAULT '3',
  `desc` varchar(1000) DEFAULT NULL,
  `raters` int(30) DEFAULT '1',
  `approved` varchar(10) DEFAULT 'no',
  PRIMARY KEY (`cid`),
  KEY `owner` (`owner`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=15 ;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`cid`, `cname`, `owner`, `start_date`, `no_of_followers`, `category`, `rating`, `desc`, `raters`, `approved`) VALUES
(1, 'xxx', 'godisdj007@gmail.com', '2013-02-20', 0, 'Random_lessons', 3, 'random lessons', 1, 'yes'),
(11, 'da', 'godisdj.cobain@gmail.com', '2013-02-12', 3, 'computer science', 3.66667, 'design and analysis of \r\nalgorithms', 3, 'yes'),
(12, 'computer networks', 'godisdj007@gmail.com', '2013-02-17', 0, 'virus', 3, 'add desc here', 1, 'no'),
(14, 'learn guitar', 'atttanwarajay@gmail.com', '2013-02-21', 1, 'arts and entertainment', 3, 'learn guitar\r\nin easy\r\nsteps', 1, 'no');

-- --------------------------------------------------------

--
-- Table structure for table `coursetags`
--

CREATE TABLE IF NOT EXISTS `coursetags` (
  `cid` int(30) NOT NULL,
  `tag` varchar(30) NOT NULL,
  `class` varchar(5) NOT NULL DEFAULT 'b',
  PRIMARY KEY (`cid`,`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `coursetags`
--

INSERT INTO `coursetags` (`cid`, `tag`, `class`) VALUES
(11, 'computer', 'b'),
(11, 'da', 'a'),
(12, 'computer', 'a'),
(12, 'networks', 'a'),
(12, 'science', 'b'),
(12, 'virus', 'a'),
(14, 'arts and entertainment', 'a'),
(14, 'cords', 'b'),
(14, 'guitar', 'a'),
(14, 'instrument', 'b'),
(14, 'music', 'b');

-- --------------------------------------------------------

--
-- Table structure for table `enrollments`
--

CREATE TABLE IF NOT EXISTS `enrollments` (
  `cid` int(30) NOT NULL,
  `uid` varchar(30) NOT NULL,
  PRIMARY KEY (`cid`,`uid`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `enrollments`
--

INSERT INTO `enrollments` (`cid`, `uid`) VALUES
(11, 'atttanwarajay@gmail.com'),
(14, 'atttanwarajay@gmail.com'),
(11, 'godisdj.cobain@gmail.com'),
(11, 'godisdj007@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `feedbacks`
--

CREATE TABLE IF NOT EXISTS `feedbacks` (
  `uid` varchar(20) NOT NULL,
  `feedback` varchar(200) DEFAULT NULL,
  `post_date` date NOT NULL,
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `forums`
--

CREATE TABLE IF NOT EXISTS `forums` (
  `fno` bigint(100) NOT NULL AUTO_INCREMENT,
  `cid` int(30) NOT NULL,
  `owner` varchar(30) NOT NULL,
  `fname` varchar(100) NOT NULL,
  `no_of_posts` int(30) NOT NULL DEFAULT '0',
  `start_date` date NOT NULL,
  PRIMARY KEY (`fno`),
  KEY `cid` (`cid`),
  KEY `owner` (`owner`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=3 ;

--
-- Dumping data for table `forums`
--

INSERT INTO `forums` (`fno`, `cid`, `owner`, `fname`, `no_of_posts`, `start_date`) VALUES
(2, 11, 'godisdj007@gmail.com', 'what is the syllabus for this course?', 0, '2013-02-12');

-- --------------------------------------------------------

--
-- Table structure for table `forumsposts`
--

CREATE TABLE IF NOT EXISTS `forumsposts` (
  `pno` bigint(30) NOT NULL AUTO_INCREMENT,
  `cid` int(30) NOT NULL,
  `fno` bigint(30) NOT NULL,
  `posted_by` varchar(30) NOT NULL,
  `posted_on` date NOT NULL,
  `likes` int(30) DEFAULT '0',
  `content` varchar(300) NOT NULL,
  PRIMARY KEY (`pno`),
  KEY `cid` (`cid`),
  KEY `fno` (`fno`),
  KEY `posted_by` (`posted_by`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `forumsposts`
--

INSERT INTO `forumsposts` (`pno`, `cid`, `fno`, `posted_by`, `posted_on`, `likes`, `content`) VALUES
(2, 11, 2, 'godisdj.cobain@gmail.com', '2013-02-13', 0, 'asldkjasdlkhdkhjdlkasjdlj'),
(3, 11, 2, 'godisdj.cobain@gmail.com', '2013-02-13', 0, 'post added 1');

-- --------------------------------------------------------

--
-- Table structure for table `lessons`
--

CREATE TABLE IF NOT EXISTS `lessons` (
  `cid` int(30) NOT NULL,
  `lno` bigint(100) NOT NULL AUTO_INCREMENT,
  `lname` varchar(50) NOT NULL,
  `ldesc` varchar(200) NOT NULL,
  `postdate` date NOT NULL,
  `filetype` varchar(40) NOT NULL,
  `filename` varchar(100) NOT NULL,
  `submitted_by` varchar(30) DEFAULT NULL,
  `likes` int(30) DEFAULT '0',
  PRIMARY KEY (`lno`),
  KEY `submitted_by` (`submitted_by`),
  KEY `cid` (`cid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `lessons`
--

INSERT INTO `lessons` (`cid`, `lno`, `lname`, `ldesc`, `postdate`, `filetype`, `filename`, `submitted_by`, `likes`) VALUES
(11, 1, 'introduction', 'this lesson gives you a brief introduction of the course', '2013-02-12', 'pdf', 'slides_algo-intro-annotated-final.pdf', 'godisdj.cobain@gmail.com', 2),
(11, 2, 'Merge Sort Motivation and Example', 'merge sort example', '2013-02-12', 'video', '1 - 3 - Merge Sort Motivation and Example (9 min).mp4', 'godisdj.cobain@gmail.com', 6),
(11, 8, 'big O notation', 'analysis with big o', '2013-02-20', 'video/mp4', '2 - 1 - Big-Oh Notation (4 min).mp4', 'godisdj007@gmail.com', 1),
(11, 9, 'big Omega notation', 'desc', '2013-02-20', 'video/mp4', '2 - 3 - Big Omega and Theta (7 min).mp4', 'godisdj.cobain@gmail.com', 1),
(14, 10, 'introduction to guitar chords', 'description', '2013-02-21', 'application/octet-stream', 'GuitarChords.flv', 'atttanwarajay@gmail.com', 0),
(14, 11, 'musical alphabets', 'whatever', '2013-02-21', 'video/mp4', '1Learn Guitar 2 Musical Alphabet.mp4', 'atttanwarajay@gmail.com', 0),
(14, 12, 'chord progressions', 'asdsad;;', '2013-02-21', 'application/pdf', 'chord-progressions-chart.pdf', 'atttanwarajay@gmail.com', 0);

-- --------------------------------------------------------

--
-- Table structure for table `lessontags`
--

CREATE TABLE IF NOT EXISTS `lessontags` (
  `lno` bigint(100) NOT NULL,
  `tag` varchar(30) NOT NULL,
  `class` varchar(5) NOT NULL DEFAULT 'b',
  PRIMARY KEY (`lno`,`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `lessontags`
--

INSERT INTO `lessontags` (`lno`, `tag`, `class`) VALUES
(8, 'algorithms', 'b'),
(8, 'analysis', 'b'),
(8, 'big', 'a'),
(8, 'notation', 'a'),
(8, 'O', 'a'),
(9, 'algorithms', 'b'),
(9, 'analysis', 'b'),
(9, 'big', 'a'),
(9, 'computer', 'b'),
(9, 'notation', 'a'),
(9, 'Omega', 'a'),
(10, 'chords', 'a'),
(10, 'guitar', 'a'),
(10, 'introduction', 'a'),
(10, 'music', 'b'),
(11, 'alphabets', 'a'),
(11, 'guitar', 'b'),
(11, 'music', 'b'),
(11, 'musical', 'a'),
(12, 'chord', 'a'),
(12, 'chords', 'b'),
(12, 'guitar', 'b'),
(12, 'progressions', 'a');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE IF NOT EXISTS `users` (
  `uid` int(30) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(20) NOT NULL,
  PRIMARY KEY (`uid`),
  KEY `email` (`email`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=16 ;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`uid`, `name`, `email`, `password`) VALUES
(1, 'devesh joshi', 'godisdj007@gmail.com', 'morzinraat'),
(10, 'dev', 'godisdj.cobain@gmail.com', 'pass'),
(15, 'ajay tanwar', 'atttanwarajay@gmail.com', 'pass');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `courses`
--
ALTER TABLE `courses`
  ADD CONSTRAINT `courses_ibfk_1` FOREIGN KEY (`owner`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `coursetags`
--
ALTER TABLE `coursetags`
  ADD CONSTRAINT `coursetags_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `enrollments`
--
ALTER TABLE `enrollments`
  ADD CONSTRAINT `enrollments_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `enrollments_ibfk_2` FOREIGN KEY (`uid`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `feedbacks`
--
ALTER TABLE `feedbacks`
  ADD CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`uid`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `forums`
--
ALTER TABLE `forums`
  ADD CONSTRAINT `forums_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `forums_ibfk_2` FOREIGN KEY (`owner`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `forumsposts`
--
ALTER TABLE `forumsposts`
  ADD CONSTRAINT `forumsposts_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `forumsposts_ibfk_2` FOREIGN KEY (`posted_by`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `forumsposts_ibfk_3` FOREIGN KEY (`fno`) REFERENCES `forums` (`fno`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `lessons`
--
ALTER TABLE `lessons`
  ADD CONSTRAINT `lessons_ibfk_2` FOREIGN KEY (`submitted_by`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `lessons_ibfk_3` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `lessontags`
--
ALTER TABLE `lessontags`
  ADD CONSTRAINT `lessontags_ibfk_1` FOREIGN KEY (`lno`) REFERENCES `lessons` (`lno`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
