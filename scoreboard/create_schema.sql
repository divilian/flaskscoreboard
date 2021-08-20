
DROP TABLE IF EXISTS `chars`;
CREATE TABLE `chars` (
  `realname` varchar(40) NOT NULL,
  `charname` varchar(40) PRIMARY KEY NOT NULL
);

DROP TABLE IF EXISTS `xp`;
CREATE TABLE `xp` (
  `username` varchar(40) NOT NULL,
  `xps` int(11) NOT NULL,
  `tag` varchar(100) DEFAULT NULL,
  `thetime` datetime DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS `secret`;
CREATE TABLE `secret` (
  `secret` varchar(40) DEFAULT NULL
);
