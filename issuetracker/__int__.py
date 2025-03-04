"""Initializes the LCC Issue Tracker Flask application.

This script runs automatically when the issuetracker module is first loaded,
and handles all the setup for our Flask app.
"""
import os
from flask import Flask

app = Flask(__name__)

# Set the "secret key" for signing session cookies
app.secret_key = 'LCC Issue Tracker Secret Key (CHANGE THIS)'

# Configure upload folder for profile images
app.config['UPLOAD_FOLDER'] = os.path.join(app.static_folder, 'images', 'profile_images')
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # Limit profile image size to 1MB

# Set up database connection
from issuetracker import connect
from issuetracker import db
db.init_db(app, connect.dbuser, connect.dbpass, connect.dbhost, connect.dbname)

# Include all modules that define our Flask route-handling functions
from issuetracker import user
from issuetracker import visitor
from issuetracker import helper
from issuetracker import admin
from issuetracker import issues