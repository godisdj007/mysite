-- phpMyAdmin SQL Dump
-- version 3.4.10.1
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Feb 23, 2013 at 09:29 AM
-- Server version: 5.5.20
-- PHP Version: 5.3.10

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `devesh mysite`
--

-- --------------------------------------------------------

--
-- Table structure for table `assignment`
--

CREATE TABLE IF NOT EXISTS `assignment` (
  `asid` bigint(100) NOT NULL AUTO_INCREMENT,
  `cid` int(30) NOT NULL,
  `assname` varchar(100) NOT NULL,
  `post_by` varchar(30) NOT NULL,
  `post_date` date NOT NULL,
  `type` text NOT NULL,
  PRIMARY KEY (`asid`),
  KEY `cid` (`cid`),
  KEY `post_by` (`post_by`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=95 ;

--
-- Dumping data for table `assignment`
--

INSERT INTO `assignment` (`asid`, `cid`, `assname`, `post_by`, `post_date`, `type`) VALUES
(1, 11, 'abcd', 'godisdj007@gmail.com', '2013-02-15', 'mcq'),
(2, 11, 'wxyz', 'attanwarajay@gmail.com', '2013-02-09', 'mcq'),
(3, 11, 'pqrs', 'godisdj.cobain@gmail.com', '2013-02-09', 'descriptive'),
(11, 11, 'New_DESCRIPTIVE', 'godisdj.cobain@gmail.com', '2013-02-18', 'descriptive'),
(12, 11, 'NEW_MCQ', 'godisdj.cobain@gmail.com', '2013-02-18', 'mcq'),
(82, 11, 'NEW_MCQ1', 'godisdj.cobain@gmail.com', '2013-02-18', 'mcq'),
(87, 11, 'MySQL', 'godisdj.cobain@gmail.com', '2013-02-18', 'mcq'),
(88, 11, 'design A& analysis MCQ', 'godisdj.cobain@gmail.com', '2013-02-19', 'mcq'),
(89, 11, 'ghfhgf', 'godisdj.cobain@gmail.com', '2013-02-19', 'descriptive'),
(90, 11, 'defgerg', 'godisdj.cobain@gmail.com', '2013-02-19', 'descriptive'),
(91, 11, 'rthgrtghrw', 'godisdj.cobain@gmail.com', '2013-02-19', 'descriptive'),
(92, 11, 'rhgkj', 'godisdj.cobain@gmail.com', '2013-02-22', 'mcq'),
(93, 11, 'typo', 'godisdj.cobain@gmail.com', '2013-02-23', 'descriptive'),
(94, 11, 'MCQ_typo', 'godisdj.cobain@gmail.com', '2013-02-23', 'mcq');

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=13 ;

--
-- Dumping data for table `courses`
--

INSERT INTO `courses` (`cid`, `cname`, `owner`, `start_date`, `no_of_followers`, `category`, `rating`, `desc`, `raters`, `approved`) VALUES
(1, 'xxx', 'godisdj007@gmail.com', '2013-02-20', 0, 'Random_lessons', 3, 'random lessons', 1, 'yes'),
(11, 'da', 'godisdj.cobain@gmail.com', '2013-02-12', 3, 'computer science', 3.66667, 'design and analysis of \r\nalgorithms', 3, 'yes'),
(12, 'computer networks', 'godisdj007@gmail.com', '2013-02-17', 1, 'virus', 3, 'add desc here', 1, 'no');

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
(12, 'virus', 'a');

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
(11, 'godisdj.cobain@gmail.com'),
(12, 'godisdj.cobain@gmail.com'),
(11, 'godisdj007@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `feedbacks`
--

CREATE TABLE IF NOT EXISTS `feedbacks` (
  `fno` bigint(100) NOT NULL AUTO_INCREMENT,
  `cid` int(30) NOT NULL,
  `user` varchar(30) NOT NULL,
  `feedback` text NOT NULL,
  `post_date` date NOT NULL,
  PRIMARY KEY (`fno`),
  KEY `cid` (`cid`),
  KEY `user` (`user`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=9 ;

--
-- Dumping data for table `feedbacks`
--

INSERT INTO `feedbacks` (`fno`, `cid`, `user`, `feedback`, `post_date`) VALUES
(1, 11, 'godisdj.cobain@gmail.com', 'rfhwrthrwet', '2013-02-19'),
(3, 11, 'godisdj.cobain@gmail.com', 'erger', '2013-02-19'),
(5, 11, 'godisdj.cobain@gmail.com', 'ergreg45t445643', '2013-02-19'),
(7, 11, 'godisdj.cobain@gmail.com', '456gh &^%&^HGvjhGJHG', '2013-02-19'),
(8, 11, 'godisdj.cobain@gmail.com', 'ferjfb', '2013-02-20');

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=4 ;

--
-- Dumping data for table `forums`
--

INSERT INTO `forums` (`fno`, `cid`, `owner`, `fname`, `no_of_posts`, `start_date`) VALUES
(2, 11, 'godisdj007@gmail.com', 'what is the syllabus for this course?', 0, '2013-02-12'),
(3, 11, 'godisdj.cobain@gmail.com', 'how to thorttle congestion on network?', 0, '2013-02-18');

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=28 ;

--
-- Dumping data for table `forumsposts`
--

INSERT INTO `forumsposts` (`pno`, `cid`, `fno`, `posted_by`, `posted_on`, `likes`, `content`) VALUES
(2, 11, 2, 'godisdj.cobain@gmail.com', '2013-02-13', 5, 'asldkjasdlkhdkhjdlkasjdlj'),
(3, 11, 2, 'godisdj.cobain@gmail.com', '2013-02-13', 5, 'post added 1'),
(4, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 4, 'm hpy'),
(15, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 3, 'thyyth'),
(16, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 3, 'dfdsgd'),
(17, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 3, 'gedrfgdfgh'),
(18, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 3, 'gfdgf;and'),
(19, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 3, 'ghjfhj;;'),
(20, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 3, 'tyutfrghfg'),
(21, 11, 2, 'godisdj007@gmail.com', '2013-02-14', 4, ''' and asjh;where'),
(22, 11, 2, 'attanwarajay@gmail.com', '2013-02-17', 2, 'dfgerthyet'),
(23, 11, 2, 'attanwarajay@gmail.com', '2013-02-17', 1, 'tyhrtyrty'),
(24, 11, 2, 'attanwarajay@gmail.com', '2013-02-17', 2, 'tyhrtyrty'),
(25, 11, 2, 'attanwarajay@gmail.com', '2013-02-17', 2, 'rterytr'),
(26, 11, 2, 'godisdj.cobain@gmail.com', '2013-02-23', 1, 'dgrtghwrtyrwtyr'),
(27, 11, 2, 'godisdj.cobain@gmail.com', '2013-02-23', 0, 'htr657567567');

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
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=10 ;

--
-- Dumping data for table `lessons`
--

INSERT INTO `lessons` (`cid`, `lno`, `lname`, `ldesc`, `postdate`, `filetype`, `filename`, `submitted_by`, `likes`) VALUES
(11, 1, 'introduction', 'this lesson gives you a brief introduction of the course', '2013-02-12', 'pdf', 'slides_algo-intro-annotated-final.pdf', 'godisdj.cobain@gmail.com', 2),
(11, 2, 'Merge Sort Motivation and Example', 'merge sort example', '2013-02-12', 'video', '1 - 3 - Merge Sort Motivation and Example (9 min).mp4', 'godisdj.cobain@gmail.com', 6),
(11, 8, 'big O notation', 'analysis with big o', '2013-02-20', 'video/mp4', '2 - 1 - Big-Oh Notation (4 min).mp4', 'godisdj007@gmail.com', 1),
(11, 9, 'big Omega notation', 'desc', '2013-02-20', 'video/mp4', '2 - 3 - Big Omega and Theta (7 min).mp4', 'godisdj.cobain@gmail.com', 1);

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
(9, 'Omega', 'a');

-- --------------------------------------------------------

--
-- Table structure for table `subscribe`
--

CREATE TABLE IF NOT EXISTS `subscribe` (
  `user` varchar(30) NOT NULL,
  `sub_user` varchar(30) NOT NULL,
  KEY `user` (`user`),
  KEY `sub_user` (`sub_user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `subscribe`
--

INSERT INTO `subscribe` (`user`, `sub_user`) VALUES
('godisdj.cobain@gmail.com', 'godisdj.cobain@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `userlikes`
--

CREATE TABLE IF NOT EXISTS `userlikes` (
  `pno` bigint(30) NOT NULL,
  `fno` bigint(30) NOT NULL,
  `cid` int(30) NOT NULL,
  `user` varchar(30) NOT NULL,
  `likes` int(1) NOT NULL,
  KEY `pno` (`pno`),
  KEY `fno` (`fno`),
  KEY `cid` (`cid`),
  KEY `user` (`user`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `userlikes`
--

INSERT INTO `userlikes` (`pno`, `fno`, `cid`, `user`, `likes`) VALUES
(4, 2, 11, 'godisdj007@gmail.com', 1),
(15, 2, 11, 'godisdj007@gmail.com', 1),
(16, 2, 11, 'godisdj007@gmail.com', 1),
(17, 2, 11, 'godisdj007@gmail.com', 1),
(18, 2, 11, 'godisdj007@gmail.com', 1),
(19, 2, 11, 'godisdj007@gmail.com', 1),
(20, 2, 11, 'godisdj007@gmail.com', 1),
(21, 2, 11, 'godisdj007@gmail.com', 1),
(3, 2, 11, 'godisdj007@gmail.com', 1),
(3, 2, 11, 'attanwarajay@gmail.com', 1),
(2, 2, 11, 'attanwarajay@gmail.com', 1),
(4, 2, 11, 'attanwarajay@gmail.com', 1),
(15, 2, 11, 'attanwarajay@gmail.com', 1),
(16, 2, 11, 'attanwarajay@gmail.com', 1),
(17, 2, 11, 'attanwarajay@gmail.com', 1),
(18, 2, 11, 'attanwarajay@gmail.com', 1),
(21, 2, 11, 'attanwarajay@gmail.com', 1),
(20, 2, 11, 'attanwarajay@gmail.com', 1),
(19, 2, 11, 'attanwarajay@gmail.com', 1),
(24, 2, 11, 'attanwarajay@gmail.com', 1),
(23, 2, 11, 'attanwarajay@gmail.com', 1),
(22, 2, 11, 'attanwarajay@gmail.com', 1),
(25, 2, 11, 'attanwarajay@gmail.com', 1),
(24, 2, 11, 'godisdj.cobain@gmail.com', 1),
(25, 2, 11, 'godisdj.cobain@gmail.com', 1),
(3, 2, 11, 'godisdj.cobain@gmail.com', 1),
(4, 2, 11, 'godisdj.cobain@gmail.com', 1),
(22, 2, 11, 'godisdj.cobain@gmail.com', 1),
(26, 2, 11, 'godisdj.cobain@gmail.com', 1),
(21, 2, 11, 'godisdj.cobain@gmail.com', 1),
(2, 2, 11, 'godisdj.cobain@gmail.com', 1);

-- --------------------------------------------------------

--
-- Table structure for table `usermarks`
--

CREATE TABLE IF NOT EXISTS `usermarks` (
  `srno` bigint(100) NOT NULL AUTO_INCREMENT,
  `asid` bigint(100) NOT NULL,
  `cid` int(30) NOT NULL,
  `user` varchar(30) NOT NULL,
  `marks` int(9) NOT NULL,
  PRIMARY KEY (`srno`),
  KEY `asid` (`asid`),
  KEY `cid` (`cid`),
  KEY `user` (`user`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=74 ;

--
-- Dumping data for table `usermarks`
--

INSERT INTO `usermarks` (`srno`, `asid`, `cid`, `user`, `marks`) VALUES
(40, 1, 11, 'godisdj007@gmail.com', 5),
(64, 1, 11, 'attanwarajay@gmail.com', 3),
(65, 82, 11, 'godisdj.cobain@gmail.com', 1),
(66, 87, 11, 'godisdj.cobain@gmail.com', 2),
(67, 88, 11, 'godisdj.cobain@gmail.com', 3),
(68, 92, 11, 'godisdj.cobain@gmail.com', 2),
(73, 1, 11, 'godisdj.cobain@gmail.com', 3);

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
(15, 'ajay', 'attanwarajay@gmail.com', '12345');

-- --------------------------------------------------------

--
-- Table structure for table `viewdescriptive`
--

CREATE TABLE IF NOT EXISTS `viewdescriptive` (
  `qno` bigint(100) NOT NULL AUTO_INCREMENT,
  `cid` int(30) NOT NULL,
  `asid` bigint(100) NOT NULL,
  `question` text NOT NULL,
  `options` text,
  `answer` text,
  PRIMARY KEY (`qno`),
  KEY `cid` (`cid`),
  KEY `asid` (`asid`)
) ENGINE=InnoDB  DEFAULT CHARSET=latin1 AUTO_INCREMENT=38 ;

--
-- Dumping data for table `viewdescriptive`
--

INSERT INTO `viewdescriptive` (`qno`, `cid`, `asid`, `question`, `options`, `answer`) VALUES
(1, 11, 3, 'how to design UML for Tranport Company?', NULL, NULL),
(3, 11, 1, 'The magic forloop variable is only available at where?', 'loop~!@string~!@while~!@if else', 'loop'),
(4, 11, 1, 'On which date application will be submit?', '22~!@24~!@12~!@4', '4'),
(5, 11, 1, 'What is port number of TCP?', '53~!@80~!@110~!@20', '20'),
(6, 11, 1, 'how to disable button in javascript after one click?', 'by JS~!@by JAVA~!@ by C++~!@by python', 'by python'),
(8, 11, 11, 'how are you?', NULL, NULL),
(9, 11, 11, 'dsfjgj', NULL, NULL),
(10, 11, 11, 'dfghrgth', NULL, NULL),
(11, 11, 11, 'fgherth', NULL, NULL),
(12, 11, 11, 'dgher', NULL, NULL),
(13, 11, 11, 'dshgrt', NULL, NULL),
(15, 11, 82, 'jdkhlkjhjl', '1~!@2~!@3~!@4', '3'),
(16, 11, 87, 'fhtyh', 'gh~!@rty~!@rty~!@rty', 'rty'),
(17, 11, 87, 'fhre', 'rty~!@3~!@rty~!@fg', 'fg'),
(18, 11, 88, 'fjghkljghkjhgkjhfdkh', '2~!@3~!@4~!@6', '4'),
(19, 11, 88, 'gfhftrghty', 'fd~!@hv~!@hg~!@jk', 'hg'),
(20, 11, 88, 'gfhftrghty', 'fd~!@hv~!@hg~!@jk', 'hg'),
(21, 11, 88, 'gfhftrghty', 'fd~!@hv~!@hg~!@jk', 'hg'),
(22, 11, 88, 'gfhftrghty', 'fd~!@hv~!@hg~!@jk', 'hg'),
(23, 11, 89, 'fghjgsrgfhrtght????', NULL, NULL),
(24, 11, 90, 'reghrt', NULL, NULL),
(25, 11, 90, 'erwgerg', NULL, NULL),
(26, 11, 90, 'wregwrt', NULL, NULL),
(27, 11, 91, 'wrthrthe', NULL, NULL),
(28, 11, 91, 'wrhwrtrwt', NULL, NULL),
(29, 11, 91, 'qwetgggnhtj', NULL, NULL),
(30, 11, 92, 'fdvmdmj', 'hgjh~!@hgj~!@hj~!@j', 'hj'),
(31, 11, 92, 'jjrgjerhj', 'jhk~!@kljl~!@jklk~!@vbv', 'jhk'),
(32, 11, 93, 'fhgretgheyrte', NULL, NULL),
(33, 11, 93, 'fgherthfghfdsgh', NULL, NULL),
(34, 11, 93, 'fghrtghsfdgwefg', NULL, NULL),
(35, 11, 93, 'fdhftghertty45y645', NULL, NULL),
(36, 11, 94, 'grrthggthrtghr?', '56~!@87~!@8~!@9', '8'),
(37, 11, 94, 'hrftghrtyhthyt?', 'fgh~!@hgj~!@hg~!@jkh', 'hgj');

--
-- Constraints for dumped tables
--

--
-- Constraints for table `assignment`
--
ALTER TABLE `assignment`
  ADD CONSTRAINT `assignment_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `assignment_ibfk_2` FOREIGN KEY (`post_by`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

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
  ADD CONSTRAINT `feedbacks_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `feedbacks_ibfk_2` FOREIGN KEY (`user`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

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
  ADD CONSTRAINT `forumsposts_ibfk_2` FOREIGN KEY (`fno`) REFERENCES `forums` (`fno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `forumsposts_ibfk_3` FOREIGN KEY (`posted_by`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

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

--
-- Constraints for table `subscribe`
--
ALTER TABLE `subscribe`
  ADD CONSTRAINT `subscribe_ibfk_1` FOREIGN KEY (`user`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `subscribe_ibfk_2` FOREIGN KEY (`sub_user`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `userlikes`
--
ALTER TABLE `userlikes`
  ADD CONSTRAINT `userlikes_ibfk_1` FOREIGN KEY (`pno`) REFERENCES `forumsposts` (`pno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `userlikes_ibfk_2` FOREIGN KEY (`fno`) REFERENCES `forums` (`fno`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `userlikes_ibfk_3` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `userlikes_ibfk_4` FOREIGN KEY (`user`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `usermarks`
--
ALTER TABLE `usermarks`
  ADD CONSTRAINT `usermarks_ibfk_1` FOREIGN KEY (`asid`) REFERENCES `assignment` (`asid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `usermarks_ibfk_2` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `usermarks_ibfk_3` FOREIGN KEY (`user`) REFERENCES `users` (`email`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `viewdescriptive`
--
ALTER TABLE `viewdescriptive`
  ADD CONSTRAINT `viewdescriptive_ibfk_1` FOREIGN KEY (`cid`) REFERENCES `courses` (`cid`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `viewdescriptive_ibfk_2` FOREIGN KEY (`asid`) REFERENCES `assignment` (`asid`) ON DELETE CASCADE ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
