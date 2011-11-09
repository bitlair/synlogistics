LOCK TABLES `accounts` WRITE;
INSERT INTO `accounts` VALUES (1,'0000','Assets','Assets',0,1,0,NULL);
INSERT INTO `accounts` VALUES (2,'0100','Accounts receivable','Receivable from customers',1,0,0,1);
INSERT INTO `accounts` VALUES (4,'0200','Current assets','Bank accounts, cash, etc',0,1,0,1);
INSERT INTO `accounts` VALUES (5,'0210','Cash','Cash',3,0,0,4);
INSERT INTO `accounts` VALUES (6,'0220','Current account','Main bank account',2,0,0,4);
INSERT INTO `accounts` VALUES (7,'0230','Savings account','Savings account',2,0,0,4);
INSERT INTO `accounts` VALUES (8,'0240','Reserve account','Reserves held for depreciation and taxes',2,0,0,4);
INSERT INTO `accounts` VALUES (9,'0300','Fixed assets','Things of value you own',0,1,0,1);
INSERT INTO `accounts` VALUES (10,'0310','Equipment','Equipment',0,0,0,9);
INSERT INTO `accounts` VALUES (11,'0320','Housing','Housing',0,0,0,9);
INSERT INTO `accounts` VALUES (12,'0330','Vehicles','Vehicles',0,0,0,9);
INSERT INTO `accounts` VALUES (13,'1000','Liabilities','Debts, unpaid bills, etc',10,1,0,NULL);
INSERT INTO `accounts` VALUES (14,'1100','Accounts payable','Unpaid bills',11,0,0,13);
INSERT INTO `accounts` VALUES (15,'1200','Taxes','Taxes you owe',10,0,0,13);
INSERT INTO `accounts` VALUES (16,'1210','VAT','VAT owed',10,0,0,15);
INSERT INTO `accounts` VALUES (18,'2000','Equity','Results',20,1,0,NULL);
INSERT INTO `accounts` VALUES (19,'2100','Opening balance','Opening balance',20,0,0,18);
INSERT INTO `accounts` VALUES (20,'4000','Expenses','Expenses',40,1,0,NULL);
INSERT INTO `accounts` VALUES (21,'4100','Taxes','Taxes paid',40,0,0,20);
INSERT INTO `accounts` VALUES (23,'4200','Products for resale','Purchases of goods for resale',40,0,0,20);
INSERT INTO `accounts` VALUES (24,'8000','Income','Income',80,1,0,NULL);
INSERT INTO `accounts` VALUES (25,'8100','Sales','All sales',80,0,0,24);
INSERT INTO `accounts` VALUES (26,'8110','Services','Services rendered',80,0,0,25);
INSERT INTO `accounts` VALUES (27,'8120','Products','Products sold',80,0,0,25);
INSERT INTO `accounts` VALUES (28,'8130','Contracts/subscription/memberships','Products with periodic invoicing',80,0,0,25);
UNLOCK TABLES;
