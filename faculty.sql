-- MySQL dump 10.13  Distrib 8.0.37, for Win64 (x86_64)
--
-- Host: localhost    Database: faculty
-- ------------------------------------------------------
-- Server version	8.0.37

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `faculty`
--

DROP TABLE IF EXISTS `faculty`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `faculty` (
  `faculty_id` int NOT NULL,
  `username` varchar(70) NOT NULL,
  `password` varchar(30) NOT NULL,
  `email` varchar(70) NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `address` text NOT NULL,
  `role` text NOT NULL,
  `member_status` enum('working','not working') DEFAULT 'working',
  `date_of_birth` date DEFAULT NULL,
  `gender` enum('Male','Female','Other') DEFAULT NULL,
  `department` varchar(100) DEFAULT NULL,
  `joining_date` date DEFAULT NULL,
  `blood_group` varchar(5) DEFAULT NULL,
  `supervisor` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`faculty_id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `faculty`
--

LOCK TABLES `faculty` WRITE;
/*!40000 ALTER TABLE `faculty` DISABLE KEYS */;
INSERT INTO `faculty` VALUES (2,'samreen','123','mdsamreen0227@gmail.com','9391935354','mangl','vij','working','2014-07-16','Female','cse','2024-05-15','b+','pushpa'),(8,'pushpa','Pushpa14','shincha0314@gmail.com','9391932536','mangalagiri','lecturer','working','2003-08-03','Female','computer science','2023-03-14','b+','samreen'),(202021,'Durga','123','anusha@codegnan.com','123123','ramalingeswar nagar 1st line ,61-9/2-15,vijayawada.','profecessor','working','1999-08-20','Female','CSE','2024-04-08','B+','anusha'),(202022,'anusha','123','anushabaditha1999@gmail.com','9999999','vij','profecessor','working','1996-06-12','Female','CSE','2024-04-09','B+','anusha'),(202023,'rishi','123','badithaanusha206@gmail.com','1234567','ramalingeswar nagar 1st line ,61-9/2-15,vijayawada.','profecessor','working','1999-08-20','Male','CSE','2024-04-09','B+','anusha'),(202031,'rishi','123','python@codegnan.com','11111111111','vij','profecessor','working','1997-07-16','Male','ECE','2023-09-18','A-','anusha');
/*!40000 ALTER TABLE `faculty` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leaveapplications`
--

DROP TABLE IF EXISTS `leaveapplications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leaveapplications` (
  `leave_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `application_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `response_date` timestamp NULL DEFAULT NULL,
  `leave_type` enum('Annual','Sick','Maternity','Paternity','Unpaid','Other') DEFAULT 'Annual',
  `allocated_leaves` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`leave_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `leaveapplications_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leaveapplications`
--

LOCK TABLES `leaveapplications` WRITE;
/*!40000 ALTER TABLE `leaveapplications` DISABLE KEYS */;
INSERT INTO `leaveapplications` VALUES (8,202021,'2024-04-24','2024-04-27','approved','2024-04-30 09:14:06',NULL,'Sick',2),(9,202022,'2024-04-25','2024-04-26','pending','2024-04-30 09:14:56',NULL,'Sick',0),(10,202023,'2024-04-29','2024-04-29','pending','2024-04-30 13:19:41',NULL,'Sick',0),(11,202021,'2024-05-11','2024-05-11','pending','2024-05-11 14:25:29',NULL,'Sick',0),(12,8,'2024-05-16','2024-05-18','pending','2024-05-16 07:38:19',NULL,'Sick',0),(13,8,'2024-05-17','2024-05-20','pending','2024-05-17 06:33:22',NULL,'Sick',0),(15,8,'2024-05-17','2024-05-19','pending','2024-05-17 06:34:58',NULL,'Sick',0);
/*!40000 ALTER TABLE `leaveapplications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workload`
--

DROP TABLE IF EXISTS `workload`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workload` (
  `workload_id` int NOT NULL AUTO_INCREMENT,
  `faculty_id` int NOT NULL,
  `workload_description` text NOT NULL,
  `submission_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `status` enum('pending','approved','rejected') NOT NULL DEFAULT 'pending',
  `dept` varchar(100) DEFAULT NULL,
  `response_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`workload_id`),
  KEY `faculty_id` (`faculty_id`),
  CONSTRAINT `workload_ibfk_1` FOREIGN KEY (`faculty_id`) REFERENCES `faculty` (`faculty_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workload`
--

LOCK TABLES `workload` WRITE;
/*!40000 ALTER TABLE `workload` DISABLE KEYS */;
INSERT INTO `workload` VALUES (3,202021,'i have to complete function concepts for cse ','2024-04-19 12:02:37','pending','cse','2024-05-16 08:18:31'),(4,2,'i have done my work','2024-05-17 06:34:09','pending','computer science','2024-05-17 06:34:09');
/*!40000 ALTER TABLE `workload` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `workload_assignment`
--

DROP TABLE IF EXISTS `workload_assignment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `workload_assignment` (
  `assignment_id` int NOT NULL AUTO_INCREMENT,
  `from_faculty_id` int DEFAULT NULL,
  `to_faculty_id` int DEFAULT NULL,
  `workload_id` int DEFAULT NULL,
  `assignment_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`assignment_id`),
  KEY `from_faculty_id` (`from_faculty_id`),
  KEY `to_faculty_id` (`to_faculty_id`),
  KEY `workload_id` (`workload_id`),
  CONSTRAINT `workload_assignment_ibfk_1` FOREIGN KEY (`from_faculty_id`) REFERENCES `faculty` (`faculty_id`),
  CONSTRAINT `workload_assignment_ibfk_2` FOREIGN KEY (`to_faculty_id`) REFERENCES `faculty` (`faculty_id`),
  CONSTRAINT `workload_assignment_ibfk_3` FOREIGN KEY (`workload_id`) REFERENCES `workload` (`workload_id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `workload_assignment`
--

LOCK TABLES `workload_assignment` WRITE;
/*!40000 ALTER TABLE `workload_assignment` DISABLE KEYS */;
INSERT INTO `workload_assignment` VALUES (17,202021,202023,3,'2024-05-04 10:54:47'),(18,202021,202023,3,'2024-05-11 09:21:23'),(19,202021,202023,3,'2024-05-16 06:24:29'),(20,202021,202023,3,'2024-05-16 06:24:35'),(21,202021,202023,3,'2024-05-16 06:24:36'),(22,202021,202023,3,'2024-05-16 06:24:43'),(23,202021,202022,3,'2024-05-16 08:18:22'),(24,202021,202022,3,'2024-05-16 08:18:23'),(25,202021,202022,3,'2024-05-16 08:18:27');
/*!40000 ALTER TABLE `workload_assignment` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-18 15:00:14
