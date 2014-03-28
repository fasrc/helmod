CREATE DATABASE modulestats;
USE modulestats;
DROP TABLE IF EXISTS log;
CREATE TABLE log (
  id INT(11) NOT NULL AUTO_INCREMENT,

  timestamp INT(11) NOT NULL,
  source ENUM('cli','lmod') NOT NULL,
  action VARCHAR(32),
  hostname VARCHAR(64),
  username VARCHAR(32),
  modulename VARCHAR(255),
  modulefname VARCHAR(255),
 
  PRIMARY KEY (id),
  INDEX source (source),
  INDEX username (username),
  INDEX modulename (modulename)
);
GRANT INSERT ON modulestats.log TO modulelogger IDENTIFIED BY ...FIXME...;
GRANT SELECT ON modulestats.log TO modulestats  IDENTIFIED BY ...FIXME...;
