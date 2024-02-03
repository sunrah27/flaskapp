DROP DATABASE IF EXISTS testdb;

CREATE DATABASE IF NOT EXISTS testdb;

USE testdb;

-- Create the user table if it does not exist
CREATE TABLE IF NOT EXISTS `user` (
  `id` MEDIUMINT(8) UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(100) DEFAULT NULL,
  `password` VARCHAR(64) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) AUTO_INCREMENT=1;

-- Create the userSalt table if it does not exist
CREATE TABLE IF NOT EXISTS `userSalt` (
  `user_id` MEDIUMINT(8) UNSIGNED NOT NULL,
  `salt` VARCHAR(64) DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_unique` (`user_id`),
  CONSTRAINT `fk_userSalt_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
);

-- Create the details table if it does not exist
CREATE TABLE IF NOT EXISTS `details` (
  `user_id` MEDIUMINT(8) UNSIGNED NOT NULL,
  `fname` VARCHAR(100) DEFAULT NULL,
  `lname` VARCHAR(100) DEFAULT NULL,
  `phone` VARCHAR(50) DEFAULT NULL,
  `email` VARCHAR(50) DEFAULT NULL,
  `address` VARCHAR(255) DEFAULT NULL,
  `postalZip` VARCHAR(10) DEFAULT NULL,
  `city` VARCHAR(50) DEFAULT NULL,
  `country` VARCHAR(50) DEFAULT NULL,
  `registration_datetime` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_unique` (`user_id`),
  UNIQUE KEY `email_unique` (`email`),
  CONSTRAINT `fk_details_user_id` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
);


CREATE VIEW test_view AS
SELECT
    u.id AS user_id,
    u.username,
    u.password,
    d.fname,
    d.lname,
    d.phone,
    d.email,
    d.address,
    d.postalZip,
    d.city,
    d.country,
    d.registration_datetime,
    us.salt,
    LENGTH(us.salt) AS salt_length
FROM
    user u
JOIN
    details d ON u.id = d.user_id
JOIN
    userSalt us ON u.id = us.user_id;