INSERT INTO `users` (`username`, `password_hash`, `email`, `role`)
VALUES
    ('visitor1', '$2b$12$hash1', 'visitor1@example.com', 'visitor'),
    ('visitor2', '$2b$12$hash2', 'visitor2@example.com', 'visitor'),
    ...
    ('helper1', '$2b$12$hash3', 'helper1@example.com', 'helper'),
    ('helper2', '$2b$12$hash4', 'helper2@example.com', 'helper'),
    ...
    ('admin1', '$2b$12$hash5', 'admin1@example.com', 'admin'),
    ('admin2', '$2b$12$hash6', 'admin2@example.com', 'admin');