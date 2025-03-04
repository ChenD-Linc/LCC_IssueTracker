-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS lcc_issue_tracker;

-- Switch to the database
USE lcc_issue_tracker;

-- Create users table
CREATE TABLE `users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL,
  `password_hash` CHAR(60) BINARY NOT NULL COMMENT 'Bcrypt Password Hash and Salt (60 bytes)',
  `email` VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321',
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `location` VARCHAR(80) NOT NULL,
  `profile_image` VARCHAR(255) NULL COMMENT 'Filename of the user''s profile image',
  `role` ENUM('visitor', 'helper', 'admin') NOT NULL,
  `status` ENUM('active', 'inactive') NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
);

-- Create issues table
CREATE TABLE `issues` (
  `issue_id` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `summary` VARCHAR(255) NOT NULL,
  `description` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('new', 'open', 'stalled', 'resolved') NOT NULL,
  PRIMARY KEY (`issue_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
);

-- Create comments table
CREATE TABLE `comments` (
  `comment_id` INT NOT NULL AUTO_INCREMENT,
  `issue_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `content` TEXT NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`comment_id`),
  FOREIGN KEY (`issue_id`) REFERENCES `issues`(`issue_id`),
  FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`)
);