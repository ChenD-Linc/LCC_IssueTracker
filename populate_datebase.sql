USE lcc_issue_tracker;

-- Insert visitor users (at least 20)
INSERT INTO `users` (`username`, `first_name`, `last_name`, `password_hash`, `email`, `location`, `role`, `status`, `profile_image`) VALUES
('visitor1', 'John', 'Doe', '$2b$12$xKC1HljdeFZTDLSN.fvdJ.1l6Q48RlKCGOWQGeRAjiJv8xCfO988e', 'visitor1@example.com', 'Lincoln', 'visitor', 'active', 'default.jpg'),
('visitor2', 'Jane', 'Smith', '$2b$12$xKC1HljdeFZTDLSN.fvdJ.1l6Q48RlKCGOWQGeRAjiJv8xCfO988e', 'visitor2@example.com', 'Christchurch', 'visitor', 'active', 'default.jpg'),
('visitor3', 'Emily', 'Johnson', '$2b$12$xKC1HljdeFZTDLSN.fvdJ.1l6Q48RlKCGOWQGeRAjiJv8xCfO988e', 'visitor3@example.com', 'Auckland', 'visitor', 'active', 'default.jpg'),
('visitor4', 'Michael', 'Williams', '$2b$12$xKC1HljdeFZTDLSN.fvdJ.1l6Q48RlKCGOWQGeRAjiJv8xCfO988e', 'visitor4@example.com', 'Wellington', 'visitor', 'active', 'default.jpg'),
('visitor5', 'Emma', 'Brown', '$2b$12$xKC1Hlj