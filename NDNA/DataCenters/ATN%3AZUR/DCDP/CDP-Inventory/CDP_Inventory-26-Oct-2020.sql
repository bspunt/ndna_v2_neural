-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: CDP
-- ------------------------------------------------------
-- Server version	10.1.26-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `CDP_Inventory`
--

DROP TABLE IF EXISTS `CDP_Inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `CDP_Inventory` (
  `Local_Hostname` varchar(100) NOT NULL,
  `Remote_Platform` varchar(7000) DEFAULT NULL,
  `Remote_cdp_neighbors` varchar(3000) DEFAULT NULL,
  `local_intf_remote_intf` varchar(5000) DEFAULT NULL,
  PRIMARY KEY (`Local_Hostname`),
  KEY `Local_Hostname` (`Local_Hostname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `CDP_Inventory`
--

LOCK TABLES `CDP_Inventory` WRITE;
/*!40000 ALTER TABLE `CDP_Inventory` DISABLE KEYS */;
INSERT INTO `CDP_Inventory` VALUES ('ch-zur-sdwanrt1\r','cisco C9300-48UN,  Capabilities: Router Switch IGMP  | Cisco C892FSP-K9,  Capabilities: Router Source-Route-Bridge Switch IGMP ',' ch-zur-sw1.corpzone.internalzone.com |  ch-mceZUE846.cablecom.net','GigabitEthernet0/0/1,  Port ID (outgoing port): FiveGigabitEthernet1/0/1 | GigabitEthernet0/0/0,  Port ID (outgoing port): GigabitEthernet0'),('ch-zur-sw1\r','cisco AIR-CAP3602I-E-K9,  Capabilities: Trans-Bridge Source-Route-Bridge IGMP  | cisco ISR4331/K9,  Capabilities: Router Switch IGMP  | cisco AIR-CAP3602I-E-K9,  Capabilities: Trans-Bridge Source-Route-Bridge IGMP ',' ch-zur-ap1.corpzone.internalzone.com |  ch-zur-sdwanrt1 |  CH-ZUR-AP02','FiveGigabitEthernet1/0/22,  Port ID (outgoing port): GigabitEthernet0 | FiveGigabitEthernet1/0/1,  Port ID (outgoing port): GigabitEthernet0/0/1 | FiveGigabitEthernet1/0/9,  Port ID (outgoing port): GigabitEthernet0');
/*!40000 ALTER TABLE `CDP_Inventory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-26 11:50:21
