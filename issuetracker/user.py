"""Handles user authentication and profile management.

This module provides route handlers for user registration, login, logout, and
profile management in the LCC Issue Tracker app.
"""
from issuetracker import app
from issuetracker import db
from flask import flash, redirect, render_template, request, session, url_for, abort
from flask_bcrypt import Bcrypt
import re
import os
from werkzeug.utils import secure_filename
import uuid

# Create an instance of Bcrypt for password hashing
flask_bcrypt = Bcrypt(app)

# Default role assigned to new users upon registration
DEFAULT_USER_ROLE = 'visitor'
DEFAULT_USER_STATUS = 'active'

# Allowed image file extensions for profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    """Check if the filename has an allowed extension."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def user_home_url():
    """Generate URL to the homepage for the currently logged-in user.
    
    If the user is not logged in, or has an invalid role, returns the URL
    for the login page instead.
    """
    role = session.get('role', None)

    if role == 'visitor':
        home_endpoint = 'visitor_home'
    elif role == 'helper':
        home_endpoint = 'helper_home'
    elif role == 'admin':
        home_endpoint = 'admin_home'
    else:
        home_endpoint = 'login'
    
    return url_for(home_endpoint)

def login_required(view):
    """Decorator to ensure a route can only be accessed by a logged-in user."""
    def wrapped_view(**kwargs):
        if 'loggedin' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    wrapped_view.__name__ = view.__name__
    return wrapped_view

def role_required(allowed_roles):
    """Decorator to ensure a route can only be accessed by users with specific roles."""
    def decorator(view):
        def wrapped_view(**kwargs):
            if 'loggedin' not in session:
                return redirect(url_for('login'))
            if session.get('role') not in allowed_roles:
                return render_template('access_denied.html'), 403
            return view(**kwargs)
        wrapped_view.__name__ = view.__name__
        return wrapped_view
    return decorator

@app.route('/')
def root():
    """Root endpoint (/)
    
    Redirects guests to the login page, and redirects logged-in users to
    their role-specific homepage.
    """
    return redirect(user_home_url())

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page endpoint.

    GET: Renders the login page.
    POST: Processes login form submission.
    """
    if 'loggedin' in session:
         return redirect(user_home_url())

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Get login details from form
        username = request.form['username']
        password = request.form['password']

        # Attempt to validate login details
        with db.get_cursor() as cursor:
            cursor.execute('''
                           SELECT user_id, username, password_hash, role, status
                           FROM users
                           WHERE username = %s;
                           ''', (username,))
            account = cursor.fetchone()
            
            if account is not None:
                # Check if account is active
                if account['status'] == 'inactive':
                    return render_template('login.html',
                                           username=username,
                                           account_inactive=True)
                
                # Check if password matches
                password_hash = account['password_hash']
                
                if flask_bcrypt.check_password_hash(password_hash, password):
                    # Save user's session data
                    session['loggedin'] = True
                    session['user_id'] = account['user_id']
                    session['username'] = account['username']
                    session['role'] = account['role']

                    return redirect(user_home_url())
                else:
                    # Password incorrect
                    return render_template('login.html',
                                           username=username,
                                           password_invalid=True)
            else:
                # Account doesn't exist
                return render_template('login.html', 
                                       username=username,
                                       username_invalid=True)

    # GET request or invalid POST
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup (registration) page endpoint.

    GET: Renders the signup form.
    POST: Processes the signup form submission.
    """
    if 'loggedin' in session:
         return redirect(user_home_url())
    
    if request.method == 'POST' and 'username' in request.form and 'email' in request.form and 'password' in request.form:
        # Get form data
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form.get('confirm_password', '')
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        location = request.form['location']

        # Initialize error variables
        username_error = None
        email_error = None
        password_error = None
        first_name_error = None
        last_name_error = None
        location_error = None

        # Check if username exists
        with db.get_cursor() as cursor:
            cursor.execute('SELECT user_id FROM users WHERE username = %s;',
                           (username,))
            account_already_exists = cursor.fetchone() is not None
        
        # Validate username
        if account_already_exists:
            username_error = 'An account already exists with this username.'
        elif len(username) > 20:
            username_error = 'Username cannot exceed 20 characters.'
        elif not re.match(r'^[A-Za-z0-9]+$', username):
            username_error = 'Username can only contain letters and numbers.'            

        # Validate email
        if len(email) > 320:
            email_error = 'Email address cannot exceed 320 characters.'
        elif not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            email_error = 'Invalid email address.'
                
        # Validate password
        if len(password) < 8:
            password_error = 'Password must be at least 8 characters long.'
        elif not re.search(r'[A-Z]', password) or not re.search(r'[a-z]', password) or not re.search(r'[0-9!@#$%^&*(),.?":{}|<>]', password):
            password_error = 'Password must include uppercase, lowercase, and at least one number or special character.'
        elif password != confirm_password:
            password_error = 'Passwords do not match.'
        
        # Validate first name
        if not first_name:
            first_name_error = 'First name is required.'
        elif len(first_name) > 50:
            first_name_error = 'First name cannot exceed 50 characters.'
        
        # Validate last name
        if not last_name:
            last_name_error = 'Last name is required.'
        elif len(last_name) > 50:
            last_name_error = 'Last name cannot exceed 50 characters.'
        
        # Validate location
        if not location:
            location_error = 'Location is required.'
        elif len(location) > 80:
            location_error = 'Location cannot exceed 80 characters.'
                
        if any([username_error, email_error, password_error, first_name_error, last_name_error, location_error]):
            # One or more errors, return to the signup form
            return render_template('signup.html',
                                  username=username,
                                  email=email,
                                  first_name=first_name,
                                  last_name=last_name,
                                  location=location,
                                  username_error=username_error,
                                  email_error=email_error,
                                  password_error=password_error,
                                  first_name_error=first_name_error,
                                  last_name_error=last_name_error,
                                  location_error=location_error)
        else:
            # All validations passed, create the new account
            password_hash = flask_bcrypt.generate_password_hash(password)
            
            with db.get_cursor() as cursor:
                cursor.execute('''
                               INSERT INTO users (username, password_hash, email, first_name, last_name, location, role, status)
                               VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                               ''',
                               (username, password_hash, email, first_name, last_name, location, DEFAULT_USER_ROLE, DEFAULT_USER_STATUS))
            
            # Registration complete
            return render_template('signup.html', signup_successful=True)            

    # GET request or invalid POST
    return render_template('signup.html')

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile page endpoint.

    GET: Displays the user's profile.
    POST: Updates the user's profile details.
    """
    # Get user profile from database
    with db.get_cursor() as cursor:
        cursor.execute('''
                      SELECT username, email, first_name, last_name, location, profile_image, role
                      FROM users 
                      WHERE user_id = %s;
                      ''',
                      (session['user_id'],))
        profile = cursor.fetchone()
    
    # Handle profile updates
    if request.method == 'POST' and 'email' in request.form:
        # Get form data
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        location = request.form['location']
        
        # Update user profile
        with db.get_cursor() as cursor:
            cursor.execute('''
                          UPDATE users 
                          SET email = %s, first_name = %s, last_name = %s, location = %s
                          WHERE user_id = %s;
                          ''',
                          (email, first_name, last_name, location, session['user_id']))
        
        # Refresh profile data
        with db.get_cursor() as cursor:
            cursor.execute('''
                          SELECT username, email, first_name, last_name, location, profile_image, role
                          FROM users 
                          WHERE user_id = %s;
                          ''',
                          (session['user_id'],))
            profile = cursor.fetchone()
        
        flash('Profile updated successfully!', 'success')
    
    return render_template('profile.html', profile=profile)

@app.route('/profile/image', methods=['GET', 'POST'])
@login_required
def profile_image():
    """User profile image management endpoint.

    GET: Displays the profile image management page.
    POST: Updates the user's profile image.
    """
    # Get current profile image
    with db.get_cursor() as cursor:
        cursor.execute('SELECT profile_image FROM users WHERE user_id = %s;',
                       (session['user_id'],))
        profile_image = cursor.fetchone()['profile_image']
    
    if request.method == 'POST':
        if 'remove_image' in request.form:
            # Remove profile image
            if profile_image:
                # Delete file if it exists
                try:
                    image_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_image)
                    if os.path.exists(image_path):
                        os.remove(image_path)
                except Exception as e:
                    app.logger.error(f"Error removing image file: {e}")
                
                # Update database
                with db.get_cursor() as cursor:
                    cursor.execute('UPDATE users SET profile_image = NULL WHERE user_id = %s;',
                                  (session['user_id'],))
                
                flash('Profile image removed successfully!', 'success')
            
        elif 'profile_image' in request.files:
            # Upload new profile image
            file = request.files['profile_image']
            
            if file.filename == '':
                flash('No file selected!', 'error')
            elif file and allowed_file(file.filename):
                # Generate unique filename
                filename = secure_filename(file.filename)
                filename = f"{uuid.uuid4().hex}_{filename}"
                
                # Ensure upload folder exists
                os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                
                # Save file
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(file_path)
                
                # Delete old image if it exists
                if profile_image:
                    try:
                        old_path = os.path.join(app.config['UPLOAD_FOLDER'], profile_image)
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    except Exception as e:
                        app.logger.error(f"Error removing old image file: {e}")
                
                # Update database
                with db.get_cursor() as cursor:
                    cursor.execute('UPDATE users SET profile_image = %s WHERE user_id = %s;',
                                  (filename, session['user_id']))
                
                flash('Profile image updated successfully!', 'success')
            else:
                flash('Invalid file type! Please upload a JPG, PNG, or GIF.', 'error')
        
        # Refresh profile image
        with db.get_cursor() as cursor:
            cursor.execute('SELECT profile_image FROM users WHERE user_id = %s;',
                          (session['user_id'],))
            profile_image = cursor.fetchone()['profile_image']
    
    return render_template('profile_image.html', profile_image=profile_image)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change password endpoint.

    GET: Displays the change password form.
    POST: Processes the change password form submission.
    """
    if request.method == 'POST':
        current_password = request.form['current_password']
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        
        # Validate current password
        with db.get_cursor() as cursor:
            cursor.execute('SELECT password_hash FROM users WHERE user_id = %s;',
                          (session['user_id'],))
            password_hash = cursor.fetchone()['password_hash']
        
        if not flask_bcrypt.check_password_hash(password_hash, current_password):
            return render_template('change_password.html', current_password_invalid=True)
        
        # Validate new password
        if len(new_password) < 8:
            return render_template('change_password.html', 
                                  new_password_error='Password must be at least 8 characters long.')
        
        if not re.search(r'[A-Z]', new_password) or not re.search(r'[a-z]', new_password) or not re.search(r'[0-9!@#$%^&*(),.?":{}|<>]', new_password):
            return render_template('change_password.html',
                                  new_password_error='Password must include uppercase, lowercase, and at least one number or special character.')
        
        if new_password == current_password:
            return render_template('change_password.html',
                                  new_password_error='New password must be different from current password.')
        
        if new_password != confirm_password:
            return render_template('change_password.html',
                                  confirm_password_error='Passwords do not match.')
        
        # Update password
        new_password_hash = flask_bcrypt.generate_password_hash(new_password)
        
        with db.get_cursor() as cursor:
            cursor.execute('UPDATE users SET password_hash = %s WHERE user_id = %s;',
                          (new_password_hash, session['user_id']))
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('profile'))
    
    return render_template('change_password.html')

@app.route('/logout')
def logout():
    """Logout endpoint.
    
    Logs the current user out and redirects to the login page.
    """
    # Remove session data
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username', None)
    session.pop('role', None)
    
    return redirect(url_for('login'))