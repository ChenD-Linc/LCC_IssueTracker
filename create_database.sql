-- Drop database if it exists and create a new one
DROP DATABASE IF EXISTS lcc_issue_tracker;
CREATE DATABASE lcc_issue_tracker;
USE lcc_issue_tracker;

-- Create the users table
CREATE TABLE `users` (
    `user_id` INT NOT NULL AUTO_INCREMENT,
    `username` VARCHAR(20) NOT NULL,
    `first_name` VARCHAR(20) NOT NULL,
    `last_name` VARCHAR(20) NOT NULL,
    `password_hash` CHAR(60) BINARY NOT NULL COMMENT 'Bcrypt Password Hash and Salt (60 bytes)',
    `email` VARCHAR(320) NOT NULL COMMENT 'Maximum email address length according to RFC5321 section 4.5.3.1 is 320 characters (64 for local-part, 1 for at sign, 255 for domain)',
    `location` VARCHAR(20) NOT NULL,
    `role` ENUM('visitor', 'helper', 'admin') NOT NULL DEFAULT 'visitor',
    `status` ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    `profile_image` VARCHAR(255) DEFAULT 'default.jpg',
    PRIMARY KEY (`user_id`),
    UNIQUE KEY `username` (`username`),
    UNIQUE KEY `email` (`email`)
);

-- Create the issues table
CREATE TABLE `issues` (
    `issue_id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `summary` VARCHAR(255) NOT NULL,
    `description` TEXT NOT NULL,
    `status` ENUM('new', 'open', 'stalled', 'resolved') NOT NULL DEFAULT 'new',
    `date_reported` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`issue_id`),
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);

-- Create the comments table
CREATE TABLE `comments` (
    `comment_id` INT NOT NULL AUTO_INCREMENT,
    `issue_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    `comment_text` TEXT NOT NULL,
    `date_commented` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`comment_id`),
    FOREIGN KEY (`issue_id`) REFERENCES `issues` (`issue_id`) ON DELETE CASCADE,
    FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
);