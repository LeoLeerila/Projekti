-- Table structure for table `tehtavat`
--

DROP TABLE IF EXISTS `tehtavat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tehtavat`
  `kysymys_vaihtoehdot` varchar(40) NOT NULL,
  `vastaus_vaihtoehdot` varchar(40) DEFAULT NULL,
  `vastaukset` varchar(40) DEFAULT NULL,

/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `tehtavat` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `tehtavat` VALUES ('mikä on 1+1?', '2,5,9,1', '2');
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;