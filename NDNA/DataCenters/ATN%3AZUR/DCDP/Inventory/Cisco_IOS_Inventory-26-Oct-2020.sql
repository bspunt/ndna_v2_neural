-- MySQL dump 10.16  Distrib 10.1.26-MariaDB, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: IOS_INVENTORY
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
-- Table structure for table `Cisco_IOS_Inventory`
--

DROP TABLE IF EXISTS `Cisco_IOS_Inventory`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Cisco_IOS_Inventory` (
  `Hostname` varchar(100) NOT NULL,
  `Local_IPs` varchar(5000) DEFAULT NULL,
  `Local_SVI_IPs` varchar(5000) DEFAULT NULL,
  `IOS_Image` varchar(200) DEFAULT NULL,
  `IOSVersion` varchar(200) DEFAULT NULL,
  `Flash` varchar(200) DEFAULT NULL,
  `SerialNo` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`Hostname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Cisco_IOS_Inventory`
--

LOCK TABLES `Cisco_IOS_Inventory` WRITE;
/*!40000 ALTER TABLE `Cisco_IOS_Inventory` DISABLE KEYS */;
INSERT INTO `Cisco_IOS_Inventory` VALUES ('ch-zur-sdwanrt1\r','84.72.224.234 | 10.129.141.2 | 1.1.1.1','','X86_64_LINUX_IOSD-UCMK9-M','16.12.02r, RELEASE SOFTWARE (fc9)\r','3258179584 bytes total','FDO2332M0NT\r'),('ch-zur-sw1\r','','192.168.3.1 | 10.196.26.1 | 10.186.128.1 | 10.186.192.1 | 10.152.225.1','CAT9K_IOSXE','16.12.3a, RELEASE SOFTWARE (fc1)\r','11353194496 bytes total','FJC2333S07C\r');
/*!40000 ALTER TABLE `Cisco_IOS_Inventory` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-10-26 11:49:07
