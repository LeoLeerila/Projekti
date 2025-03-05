-- Table structure for table `tehtavat`
--

DROP TABLE IF EXISTS `tehtavat`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tehtavat`
  `kysymysnumero` int(20) NOT NULL,
  `kysymys_vaihtoehdot` varchar(40) NOT NULL,
  `vastaus_vaihtoehdot` varchar(40) DEFAULT NULL,
  `vastaukset` varchar(40) DEFAULT NULL,
    REFERENCES `tehtavat`
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `game`
--

LOCK TABLES `tehtavat` WRITE;
/*!40000 ALTER TABLE `game` DISABLE KEYS */;
INSERT INTO `tehtavat` VALUES ('1', 'miksi matkaan thaimaaseen?', 'uuden vaimon takia, äijien bilereissun takia,', 'kauniin kulttuurin takia', 'kauniin kulttuurin takia');
/*!40000 ALTER TABLE `game` ENABLE KEYS */;
UNLOCK TABLES;