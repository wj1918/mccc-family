from django.db import models

class McccLibrary(models.Model):
    itemtype = models.CharField(db_column='Type', max_length=17)  # Field name made lowercase.
    classnumber = models.CharField(db_column='ClassNumber', max_length=20, blank=True)  # Field name made lowercase.
    volume = models.CharField(db_column='Volume', max_length=8, blank=True)  # Field name made lowercase.
    author = models.CharField(db_column='Author', max_length=160, blank=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=400, blank=True)  # Field name made lowercase.
    autocounter = models.IntegerField(db_column='AutoCounter', blank=True, null=True)  # Field name made lowercase.
    clutternumber = models.CharField(db_column='ClutterNumber', max_length=12, blank=True)  # Field name made lowercase.
    keeper = models.CharField(db_column='Keeper', max_length=40, blank=True)  # Field name made lowercase.
    keeperindex = models.IntegerField(db_column='KeeperIndex', blank=True, null=True)  # Field name made lowercase.
    inputdate = models.CharField(db_column='InputDate', max_length=30, blank=True)  # Field name made lowercase.
    application = models.CharField(db_column='Application', max_length=100, blank=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MCCC_Library'


"""

CREATE TABLE IF NOT EXISTS `MCCC_Library` (
   `id` int(10) NOT NULL auto_increment,
   PRIMARY KEY  (`id`), 
  `Type` varchar(17) NOT NULL DEFAULT '',
  `ClassNumber` varchar(20) DEFAULT NULL,
  `Volume` varchar(8) DEFAULT NULL,
  `Author` varchar(160) DEFAULT NULL,
  `Title` varchar(400) DEFAULT NULL,
  `AutoCounter` int(11) DEFAULT NULL,
  `ClutterNumber` varchar(12) DEFAULT NULL,
  `Keeper` varchar(40) DEFAULT NULL,
  `KeeperIndex` int(11) DEFAULT NULL,
  `InputDate` varchar(30) DEFAULT NULL,
  `Application` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


INSERT INTO  `MCCC_Library` (  
    `Type`, 
    `ClassNumber`, 
    `Volume`, 
    `Author`, 
    `Title`, 
    `AutoCounter`, 
    `ClutterNumber`, 
    `Keeper`, 
    `KeeperIndex`, 
    `InputDate` , 
    `Application` )
SELECT 'Chinese Book' AS `Type`,
       `MCCC_Library_CB-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_CB-DB`.`Volume` AS `Volume`,
       `MCCC_Library_CB-DB`.`Author` AS `Author`,
       `MCCC_Library_CB-DB`.`Title` AS `Title`,
       `MCCC_Library_CB-DB`.`AutoCounter` AS `AutoCounter`,
       `MCCC_Library_CB-DB`.`ClutterNumber` AS `ClutterNumber`,
       `MCCC_Library_CB-DB`.`Keeper` AS `Keeper`,
       `MCCC_Library_CB-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_CB-DB`.`InputDate` AS `InputDate`
       ,''     AS `Application` 
FROM `MCCC_Library_CB-DB`
UNION
SELECT 'Chinese CD' AS `Type`,
       `MCCC_Library_CCD-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_CCD-DB`.`Volume` AS `Volume`,
       `MCCC_Library_CCD-DB`.`Author` AS `Author`,
       `MCCC_Library_CCD-DB`.`Title` AS `Title`,
       `MCCC_Library_CCD-DB`.`AutoCounter` AS `AutoCounter`,
       `MCCC_Library_CCD-DB`.`ClutterNumber` AS `ClutterNumber`,
       `MCCC_Library_CCD-DB`.`Keeper` AS `Keeper`,
       `MCCC_Library_CCD-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_CCD-DB`.`InputDate` AS `InputDate`
       ,''     AS `Application` 
FROM `MCCC_Library_CCD-DB`
UNION
SELECT 'Chinese DVD' AS `Type`,
       `MCCC_Library_CDVD-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_CDVD-DB`.`Volume` AS `Volume`,
       `MCCC_Library_CDVD-DB`.`Author` AS `Author`,
       `MCCC_Library_CDVD-DB`.`Title` AS `Title`,
       `MCCC_Library_CDVD-DB`.`AutoCounter` AS `AutoCounter`,
       `MCCC_Library_CDVD-DB`.`ClutterNumber` AS `ClutterNumber`,
       `MCCC_Library_CDVD-DB`.`Keeper` AS `Keeper`,
       `MCCC_Library_CDVD-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_CDVD-DB`.`InputDate` AS `InputDate`
       ,''     AS `Application` 
FROM `MCCC_Library_CDVD-DB`
UNION
SELECT 'English Book' AS `Type`,
       `MCCC_Library_EB-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_EB-DB`.`Volume` AS `Volume`,
       `MCCC_Library_EB-DB`.`Author` AS `Author`,
       `MCCC_Library_EB-DB`.`Title` AS `Title`,
       `MCCC_Library_EB-DB`.`AutoCounter` AS `AutoCounter`,
       '' AS `ClutterNumber`,
       `MCCC_Library_EB-DB`.`Keeper` AS `Keeper`,
       `MCCC_Library_EB-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_EB-DB`.`InputDate` AS `InputDate`,
       `MCCC_Library_EB-DB`.`Application`   AS `Application` 
FROM `MCCC_Library_EB-DB`
UNION
SELECT 'English DVD' AS `Type`,
       `MCCC_Library_EDVD-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_EDVD-DB`.`Volume` AS `Volume`,
       `MCCC_Library_EDVD-DB`.`Author` AS `Author`,
       `MCCC_Library_EDVD-DB`.`Title` AS `Title`,
       `MCCC_Library_EDVD-DB`.`AutoCounter` AS `AutoCounter`,
       `MCCC_Library_EDVD-DB`.`ClutterNumber` AS `ClutterNumber`,
       `MCCC_Library_EDVD-DB`.`Keeper` AS `Keeper`,
       `MCCC_Library_EDVD-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_EDVD-DB`.`InputDate` AS `InputDate`
       ,''     AS `Application` 
FROM `MCCC_Library_EDVD-DB`
UNION
SELECT 'Kids Chinese DVD' AS `Type`,
       `MCCC_Library_KCDVD-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_KCDVD-DB`.`Volume` AS `Volume`,
       `MCCC_Library_KCDVD-DB`.`Author` AS `Author`,
       `MCCC_Library_KCDVD-DB`.`Title` AS `Title`,
       `MCCC_Library_KCDVD-DB`.`AutoCounter` AS `AutoCounter`,
       `MCCC_Library_KCDVD-DB`.`ClutterNumber` AS `ClutterNumber`,
       `MCCC_Library_KCDVD-DB`.`Keeper` AS `Keeper`,
       `MCCC_Library_KCDVD-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_KCDVD-DB`.`InputDate` AS `InputDate`
       ,''     AS `Application` 
FROM `MCCC_Library_KCDVD-DB`
UNION
SELECT 'Kids English Book' AS `Type`,
       `MCCC_Library_KEB-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_KEB-DB`.`Volume` AS `Volume`,
       `MCCC_Library_KEB-DB`.`Author` AS `Author`,
       `MCCC_Library_KEB-DB`.`Title` AS `Title`,
       `MCCC_Library_KEB-DB`.`AutoCounter` AS `AutoCounter`,
       '' AS `ClutterNumber`,
       '' AS `Keeper`,
       `MCCC_Library_KEB-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_KEB-DB`.`InputDate` AS `InputDate`
       ,''     AS `Application` 
FROM `MCCC_Library_KEB-DB`
UNION
SELECT 'Kids English DVD' AS `Type`,
       `MCCC_Library_KEDVD-DB`.`ClassNumber` AS `ClassNumber`,
       `MCCC_Library_KEDVD-DB`.`Volume` AS `Volume`,
       `MCCC_Library_KEDVD-DB`.`Author` AS `Author`,
       `MCCC_Library_KEDVD-DB`.`Title` AS `Title`,
       `MCCC_Library_KEDVD-DB`.`AutoCounter` AS `AutoCounter`,
       `MCCC_Library_KEDVD-DB`.`ClutterNumber` AS `ClutterNumber`,
       `MCCC_Library_KEDVD-DB`.`Keeper` AS `Keeper`,
       `MCCC_Library_KEDVD-DB`.`KeeperIndex` AS `KeeperIndex`,
       `MCCC_Library_KEDVD-DB`.`InputDate` AS `InputDate`
       ,''     AS `Application` 
FROM `MCCC_Library_KEDVD-DB`;

"""
