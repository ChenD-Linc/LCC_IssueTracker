-- Switch to the database
USE lcc_issue_tracker;

-- Insert visitor users (20 required)
INSERT INTO `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`, `location`, `profile_image`, `role`, `status`)
VALUES
    ('visitor1', '$2b$12$q2oXFNwVV8lHtA7kq4N4BuuXR5j1iWGvZTJGPRMuuKX0OAFQ9MnN2', 'visitor1@example.com', 'John', 'Doe', 'Christchurch', NULL, 'visitor', 'active'),
    ('visitor2', '$2b$12$8YyuI83uUyDZUDwUOFoZruFRb4DChOIJv0l8sQ41L4HrRz9oe.oPi', 'visitor2@example.com', 'Jane', 'Smith', 'Lincoln, Canterbury', NULL, 'visitor', 'active'),
    ('visitor3', '$2b$12$7CcD9VZU.6TY/3Fo7cZPVeZQ5pXDiBSfuF8ZKOBdG4PQl/28DWyCm', 'visitor3@example.com', 'Robert', 'Johnson', 'Auckland', NULL, 'visitor', 'active'),
    ('visitor4', '$2b$12$IlVcXDFmvEIR/YO5g1Df9.kLpxo4TyBJaC3Z.HPT8TGLt3UzgRxQq', 'visitor4@example.com', 'Emily', 'Williams', 'Wellington', NULL, 'visitor', 'active'),
    ('visitor5', '$2b$12$2HmcmMsaQTh6b0A.s.p4Ue5z4t7dPnrWrPhRTKhBYuxI2aYTm/xYW', 'visitor5@example.com', 'Michael', 'Brown', 'Dunedin', NULL, 'visitor', 'active'),
    ('visitor6', '$2b$12$m/9aEg4OigZLSGawlDnEuO8XMGiWJEVlXdVQCChFhw9DxYLAJ39bS', 'visitor6@example.com', 'Sara', 'Jones', 'Hamilton', NULL, 'visitor', 'active'),
    ('visitor7', '$2b$12$5MvpZkS/XKNhZBGsFZuZu.kzkZVrj.jcdWuMxn2pXfjF1FqMoZZi6', 'visitor7@example.com', 'David', 'Miller', 'Queenstown', NULL, 'visitor', 'active'),
    ('visitor8', '$2b$12$H0JtNbB7XKC1Vz1JNgG.kOIgQU1TDZXFJPEeJ.WKfN4EAEdT8I7QW', 'visitor8@example.com', 'Elizabeth', 'Davis', 'Tauranga', NULL, 'visitor', 'active'),
    ('visitor9', '$2b$12$Ktt5a4IM2h45aVAu2aZDOuwS.2HGnNqr9.Qz55QxswWo9uZF1NnW.', 'visitor9@example.com', 'James', 'Garcia', 'Nelson', NULL, 'visitor', 'active'),
    ('visitor10', '$2b$12$sZ4IQLGDyoA/k/KdFB.Ete/Zeo8zIKGd3MFr2lNexlxGLR.bMT0b2', 'visitor10@example.com', 'Jennifer', 'Rodriguez', 'Napier', NULL, 'visitor', 'active'),
    ('visitor11', '$2b$12$TDVgEF8XxSxasSQRH7oQKO1Qd/MpYNI1wU7QTqUNjz3MQuAJmm9PO', 'visitor11@example.com', 'Charles', 'Wilson', 'New Zealand', NULL, 'visitor', 'active'),
    ('visitor12', '$2b$12$UJgDf6NW19v.w7X7P.jl9uuAJFQ.6TxjNw6vbG5jU3ynQgFqy15qC', 'visitor12@example.com', 'Patricia', 'Martinez', 'UK', NULL, 'visitor', 'active'),
    ('visitor13', '$2b$12$U.NMwtFUWKK.yq55V4Jb9OYWzLiYR9/iKz.k4vSSo7xK3A5N34iPK', 'visitor13@example.com', 'George', 'Anderson', 'Lincoln', NULL, 'visitor', 'active'),
    ('visitor14', '$2b$12$4ZI7LuMxEJXYFrH5XhqF1.Ns.xqIBdtPJfBZZZqKwj.W2lhxlY12e', 'visitor14@example.com', 'Nancy', 'Thomas', 'Timaru', NULL, 'visitor', 'active'),
    ('visitor15', '$2b$12$DRwZQ5KQxVB/X4bYJ.JX7OnQAyZdNt47xQsLwlSKBzneFqOm8zHV.', 'visitor15@example.com', 'Kevin', 'Jackson', 'Canterbury', NULL, 'visitor', 'active'),
    ('visitor16', '$2b$12$2T3G3HLAzGAJ1Q8yR4Fa9e8AXbOXDLcqLDGBLzYq6xJIxGHT0ZElu', 'visitor16@example.com', 'Lisa', 'White', 'West Coast', NULL, 'visitor', 'active'),
    ('visitor17', '$2b$12$y7YUj.6p25z4VYl3Xb0zz.1I8j6NlXWwxP1JKGEf8eUMp.1i6p2Za', 'visitor17@example.com', 'Thomas', 'Harris', 'Australia', NULL, 'visitor', 'active'),
    ('visitor18', '$2b$12$jsjXtR31Hbq7HLs8/EbdL.H5m82GrZV/JCZF0R2KeBEyqYQHCiBcW', 'visitor18@example.com', 'Betty', 'Martin', 'Ashburton', NULL, 'visitor', 'active'),
    ('visitor19', '$2b$12$JkAaX9Vqe3Roz/9hE2Ypqe8kjqUB7mVCZQnBIbp7D9XHBQIXsZ.Hm', 'visitor19@example.com', 'Donald', 'Thompson', 'Singapore', NULL, 'visitor', 'active'),
    ('visitor20', '$2b$12$vSNRF8hd8v9b0OVnOEh6neTDJ1PzjFnHRl4h7Dxrx6rP5YIWgb3P.', 'visitor20@example.com', 'Margaret', 'Lewis', 'Lincoln', NULL, 'visitor', 'active');

-- Insert helper users (5 required)
INSERT INTO `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`, `location`, `profile_image`, `role`, `status`)
VALUES
    ('helper1', '$2b$12$Fzl87I3KfuaM.Y3xfj/YSuB5DfM2SgQnQXOcU/5U5nrqEDR6BF3.W', 'helper1@lcc.org', 'Stephen', 'Clark', 'Lincoln', NULL, 'helper', 'active'),
    ('helper2', '$2b$12$QXlHBMDR81nCNc5F9/qm4.BzCl.vn5YRO1.YEdGD/DQqCVNXp8RRq', 'helper2@lcc.org', 'Mary', 'Walker', 'Lincoln', NULL, 'helper', 'active'),
    ('helper3', '$2b$12$XMbqIJtOnDvzxwT4RKQ8a.dxJNT4cDX4XFw/6JVXH.Mw3lXMuZ.8q', 'helper3@lcc.org', 'Paul', 'Hall', 'Christchurch', NULL, 'helper', 'active'),
    ('helper4', '$2b$12$UTjkbViBKXCbQEOhKzHs5uCiPm7RjsxcNhBPdwXmrDiIfIyLtU5jK', 'helper4@lcc.org', 'Karen', 'Young', 'Lincoln', NULL, 'helper', 'active'),
    ('helper5', '$2b$12$wqQF/pF1g9lZ4rKCwJuCJ.gGGNYYJOvvw0gUhF16W8KRnAPVvMg3q', 'helper5@lcc.org', 'Joseph', 'Allen', 'Rolleston', NULL, 'helper', 'active');

-- Insert admin users (2 required)
INSERT INTO `users` (`username`, `password_hash`, `email`, `first_name`, `last_name`, `location`, `profile_image`, `role`, `status`)
VALUES
    ('admin1', '$2b$12$8Rl7eSmXSrqe8QqkGVE/FuiVXbJvSDiJINOZRCQRkRAtlRi/X9Biy', 'admin1@lcc.org', 'William', 'Wright', 'Lincoln', NULL, 'admin', 'active'),
    ('admin2', '$2b$12$21x6hLu43IoPRaBi7LtxL.Ae0ZQV59V.QKBj.cHt3.YmHfL9.p53G', 'admin2@lcc.org', 'Susan', 'Scott', 'Christchurch', NULL, 'admin', 'active');

-- Insert issues (20 required)
INSERT INTO `issues` (`user_id`, `summary`, `description`, `created_at`, `status`)
VALUES
    (1, 'Blocked toilet in North Block', 'The second toilet in the north block is completely blocked and unusable.', '2024-12-10 08:23:15', 'new'),
    (2, 'Fire pit damaged at site 4', 'Some of the rocks around the fire pit in site 4 are missing, leaving it unsafe to use.', '2024-12-11 14:35:22', 'open'),
    (3, 'No hot water in shower block', 'There is no hot water in any of the showers in the main shower block.', '2024-12-12 18:45:33', 'stalled'),
    (4, 'Broken bench at picnic area', 'The wooden bench near the eastern picnic area has a broken seat plank.', '2024-12-13 09:12:47', 'resolved'),
    (5, 'WiFi not working', 'Unable to connect to campground WiFi since yesterday evening.', '2024-12-14 11:28:59', 'new'),
    (6, 'Fallen tree blocking path', 'A tree has fallen and is blocking the walking path to the river.', '2024-12-15 16:37:14', 'open'),
    (7, 'Charging station not working', 'The solar charging station near site 7 doesn\'t seem to be charging devices.', '2024-12-16 13:42:05', 'stalled'),
    (8, 'Water leak at main tap', 'There\'s a significant water leak from the main tap near the cooking area.', '2024-12-17 10:15:30', 'resolved'),
    (9, 'Noisy generator from neighboring site', 'The campers at site 12 are running a very loud generator late into the night.', '2024-12-18 22:07:11', 'new'),
    (10, 'Garbage bin overflow', 'The garbage bins near the entrance are overflowing and need emptying.', '2024-12-19 07:58:23', 'open'),
    (11, 'BBQ gas bottle empty', 'The gas bottle for the BBQ area is empty and needs replacement.', '2024-12-20 17:33:45', 'resolved'),
    (12, 'Camping spot flooding', 'After last night\'s rain, site 15 is completely flooded and unusable.', '2024-12-21 08:19:27', 'new'),
    (13, 'Missing campfire tongs', 'The metal tongs used for the communal fire pit are missing.', '2024-12-22 19:24:36', 'open'),
    (14, 'Broken shower head', 'The shower head in the first cubicle of the women\'s block has broken off.', '2024-12-23 14:51:09', 'stalled'),
    (15, 'Need more firewood', 'The firewood pile for the communal areas is almost depleted.', '2024-12-24 16:22:17', 'resolved'),
    (16, 'Slippery path to river', 'The dirt path leading to the river has become very slippery and dangerous.', '2024-12-25 11:45:33', 'new'),
    (17, 'Lighting failure in facilities block', 'The lights in the main facilities block are not working.', '2024-12-26 20:17:42', 'open'),
    (18, 'Wasp nest by picnic area', 'There appears to be a wasp nest forming under the table in the main picnic area.', '2024-12-27 13:38:51', 'stalled'),
    (19, 'Recycling bins needed', 'We need dedicated recycling bins as everything is going into general waste.', '2024-12-28 09:29:04', 'new'),
    (20, 'Water pressure low', 'Water pressure in all taps has been very low since this morning.', '2024-12-29 15:13:22', 'open');

-- Insert comments (20 required, with some issues having multiple comments and some having none)
INSERT INTO `comments` (`issue_id`, `user_id`, `content`, `created_at`)
VALUES
    (1, 21, 'I\'ll check this today and see if we can unblock it.', '2024-12-10 09:30:45'),
    (1, 1, 'Thank you! It\'s becoming quite an issue for everyone in the north area.', '2024-12-10 10:15:22'),
    (1, 21, 'I\'ve attempted to unblock it but will need specialized equipment. I\'ve ordered what we need.', '2024-12-10 14:45:33'),
    
    (2, 22, 'I\'ve inspected the fire pit. We\'ll need to replace at least 5 rocks. Will do this tomorrow.', '2024-12-11 15:20:10'),
    (2, 2, 'Great, thanks for the quick response!', '2024-12-11 16:05:47'),
    
    (3, 23, 'The hot water system needs a new part. We\'ve ordered it but it won\'t arrive until next week.', '2024-12-12 19:30:12'),
    
    (4, 24, 'I\'ve replaced the broken plank on the bench. It should be safe to use now.', '2024-12-13 11:45:30'),
    (4, 4, 'Thank you! The bench looks great now.', '2024-12-13 13:20:15'),
    
    (5, 25, 'I\'ll reset the router and check the connections.', '2024-12-14 12:15:40'),
    
    (6, 26, 'I\'ll bring a chainsaw tomorrow morning to clear the path.', '2024-12-15 17:10:25'),
    
    (8, 22, 'I\'ve fixed the leak by replacing the washer. All good now.', '2024-12-17 11:30:18'),
    
    (10, 23, 'I\'ve emptied the bins and added an extra bin for the weekend.', '2024-12-19 09:15:30'),
    
    (11, 24, 'Gas bottle has been replaced and the BBQ is ready to use again.', '2024-12-20 18:45:12'),
    
    (13, 25, 'I\'ve found some temporary replacements. New ones have been ordered.', '2024-12-22 20:10:05'),
    
    (15, 26, 'Additional firewood has been delivered and stacked.', '2024-12-24 17:30:22'),
    
    (17, 21, 'Looks like a circuit breaker has tripped. I\'ve reset it and the lights are working again.', '2024-12-26 21:05:18'),
    
    (19, 22, 'Good suggestion. I\'ll get some recycling bins delivered this week.', '2024-12-28 10:20:15'),
    
    (20, 23, 'I\'ve identified a partial blockage in the main water line. Working on it now.', '2024-12-29 16:05:30'),
    (20, 20, 'Thank you for looking into this so quickly!', '2024-12-29 16:30:42'),
    (20, 23, 'The blockage has been cleared and water pressure should be back to normal now.', '2024-12-29 18:15:10');