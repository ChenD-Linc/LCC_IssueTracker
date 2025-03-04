"""Script to generate password hashes for user accounts in the LCC Issue Tracker.

This script will generate bcrypt password hashes for all user accounts you wish
to include in your database population script. Each user account should have a
unique password.

Before running this script, make sure you've installed flask_bcrypt.
"""
from collections import namedtuple
from flask import Flask
from flask_bcrypt import Bcrypt

# A simple "User Account" class to store username and password
UserAccount = namedtuple('UserAccount', ['username', 'password'])

app = Flask(__name__)
flask_bcrypt = Bcrypt(app)

# Define the users for which to generate password hashes
users = [
    # Visitors (20)
    UserAccount('visitor1', 'Visitor1Pass!'),
    UserAccount('visitor2', 'Visitor2Pass!'),
    UserAccount('visitor3', 'Visitor3Pass!'),
    UserAccount('visitor4', 'Visitor4Pass!'),
    UserAccount('visitor5', 'Visitor5Pass!'),
    UserAccount('visitor6', 'Visitor6Pass!'),
    UserAccount('visitor7', 'Visitor7Pass!'),
    UserAccount('visitor8', 'Visitor8Pass!'),
    UserAccount('visitor9', 'Visitor9Pass!'),
    UserAccount('visitor10', 'Visitor10Pass!'),
    UserAccount('visitor11', 'Visitor11Pass!'),
    UserAccount('visitor12', 'Visitor12Pass!'),
    UserAccount('visitor13', 'Visitor13Pass!'),
    UserAccount('visitor14', 'Visitor14Pass!'),
    UserAccount('visitor15', 'Visitor15Pass!'),
    UserAccount('visitor16', 'Visitor16Pass!'),
    UserAccount('visitor17', 'Visitor17Pass!'),
    UserAccount('visitor18', 'Visitor18Pass!'),
    UserAccount('visitor19', 'Visitor19Pass!'),
    UserAccount('visitor20', 'Visitor20Pass!'),
    
    # Helpers (5)
    UserAccount('helper1', 'Helper1Pass!'),
    UserAccount('helper2', 'Helper2Pass!'),
    UserAccount('helper3', 'Helper3Pass!'),
    UserAccount('helper4', 'Helper4Pass!'),
    UserAccount('helper5', 'Helper5Pass!'),
    
    # Admins (2)
    UserAccount('admin1', 'Admin1Pass!'),
    UserAccount('admin2', 'Admin2Pass!')
]

print('Username | Password | Hash | Password Matches Hash')

for user in users:
    # Generate a bcrypt hash using the default settings
    password_hash = flask_bcrypt.generate_password_hash(user.password)
    
    # Check whether the hash matches the original password
    password_matches_hash = flask_bcrypt.check_password_hash(password_hash, user.password)

    # Output username, password, hash, and verification result
    print(f'{user.username} | {user.password} | {password_hash.decode()} | {password_matches_hash}')