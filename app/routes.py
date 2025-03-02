from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import (RegistrationForm, LoginForm, UpdateProfileForm, ChangePasswordForm,
                      ReportIssueForm, AddCommentForm, ChangeIssueStatusForm, 
                      UserRoleForm, UserStatusForm, SearchUserForm)
from app.models import User, Issue, Comment
from app.utils import save_profile_picture, delete_profile_picture
from flask_login import login_user, current_user, logout_user, login_required
import os

# Home route
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', title='LCC Issue Tracker')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            location=form.location.data,
            role='visitor',
            status='active',
            profile_image='default.jpg'
        )
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password_hash, form.password.data):
            if user.status == 'inactive':
                flash('Your account has been deactivated. Please contact an administrator.', 'danger')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    return render_template('login.html', title='Login', form=form)

# Logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Profile route
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.profile_image.data:
            # Delete old profile image if not default
            if current_user.profile_image != 'default.jpg':
                delete_profile_picture(current_user.profile_image)
            
            # Save new profile image
            picture_file = save_profile_picture(form.profile_image.data)
            current_user.profile_image = picture_file
        
        # Update user information
        current_user.email = form.email.data
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.location = form.location.data
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.location.data = current_user.location
    
    return render_template('profile.html', title='Profile', form=form)

# Remove profile image route
@app.route('/remove_profile_image', methods=['POST'])
@login_required
def remove_profile_image():
    if current_user.profile_image != 'default.jpg':
        delete_profile_picture(current_user.profile_image)
        current_user.profile_image = 'default.jpg'
        db.session.commit()
        flash('Your profile image has been removed!', 'success')
    return redirect(url_for('profile'))

# Change password route
@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password_hash, form.current_password.data):
            # Check if new password is different from current password
            if form.current_password.data == form.new_password.data:
                flash('New password must be different from current password', 'danger')
                return redirect(url_for('change_password'))
            
            # Update password
            hashed_password = bcrypt.generate_password_hash(form.new_password.data).decode('utf-8')
            current_user.password_hash = hashed_password
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('profile'))
        else:
            flash('Current password is incorrect', 'danger')
    return render_template('change_password.html', title='Change Password', form=form)

# Report issue route
@app.route('/report_issue', methods=['GET', 'POST'])
@login_required
def report_issue():
    form = ReportIssueForm()
    if form.validate_on_submit():
        issue = Issue(
            summary=form.summary.data,
            description=form.description.data,
            status='new',
            reporter=current_user
        )
        db.session.add(issue)
        db.session.commit()
        flash('Your issue has been reported!', 'success')
        return redirect(url_for('view_own_issues'))
    return render_template('report_issue.html', title='Report Issue', form=form)

# View own issues route
@app.route('/view_own_issues')
@login_required
def view_own_issues():
    issues = Issue.query.filter_by(user_id=current_user.user_id).order_by(Issue.date_reported.desc()).all()
    return render_template('view_issues.html', title='My Issues', issues=issues, own_issues=True)

# View single issue route
@app.route('/issue/<int:issue_id>', methods=['GET', 'POST'])
@login_required
def view_issue(issue_id):
    issue = Issue.query.get_or_404(issue_id)
    
    # Check if user has permission to view this issue
    if issue.user_id != current_user.user_id and current_user.role not in ['helper', 'admin']:
        abort(403)
    
    # Get comments for this issue
    comments = Comment.query.filter_by(issue_id=issue.issue_id).order_by(Comment.date_commented).all()
    
    # Add comment form
    comment_form = AddCommentForm()
    
    # Status change form (for helpers and admins only)
    status_form = None
    if current_user.role in ['helper', 'admin']:
        status_form = ChangeIssueStatusForm()
        status_form.status.data = issue.status
    
    # Process comment submission
    if comment_form.validate_on_submit():
        comment = Comment(
            comment_text=comment_form.comment_text.data,
            issue_id=issue.issue_id,
            user_id=current_user.user_id
        )
        db.session.add(comment)
        
        # If helper/admin comments on new, stalled, or resolved issue, automatically set to open
        if current_user.role in ['helper', 'admin'] and issue.status in ['new', 'stalled', 'resolved']:
            issue.status = 'open'
        
        db.session.commit()
        flash('Your comment has been added!', 'success')
        return redirect(url_for('view_issue', issue_id=issue.issue_id))
    
    return render_template('view_comments.html', title=issue.summary, issue=issue, 
                          comments=comments, comment_form=comment_form, status_form=status_form)

# Change issue status route (helper & admin only)
@app.route('/change_status/<int:issue_id>', methods=['POST'])
@login_required
def change_status(issue_id):
    if current_user.role not in ['helper', 'admin']:
        abort(403)
        
    issue = Issue.query.get_or_404(issue_id)
    form = ChangeIssueStatusForm()
    
    if form.validate_on_submit():
        issue.status = form.status.data
        db.session.commit()
        flash(f'Issue status updated to {form.status.data}!', 'success')
    
    return redirect(url_for('view_issue', issue_id=issue.issue_id))

# View all issues route (helper & admin only)
@app.route('/all_issues')
@login_required
def all_issues():
    if current_user.role not in ['helper', 'admin']:
        abort(403)
        
    active_issues = Issue.query.filter(Issue.status.in_(['new', 'open', 'stalled'])).order_by(Issue.date_reported.desc()).all()
    resolved_issues = Issue.query.filter_by(status='resolved').order_by(Issue.date_reported.desc()).all()
    
    return render_template('all_issues.html', title='All Issues', 
                          active_issues=active_issues, resolved_issues=resolved_issues)

# Admin routes - User management
@app.route('/manage_users', methods=['GET', 'POST'])
@login_required
def manage_users():
    if current_user.role != 'admin':
        abort(403)
    
    form = SearchUserForm()
    search_query = ''
    
    if form.validate_on_submit():
        search_query = form.search.data
        users = User.query.filter(
            (User.username.like(f'%{search_query}%')) | 
            (User.first_name.like(f'%{search_query}%')) | 
            (User.last_name.like(f'%{search_query}%'))
        ).all()
    else:
        users = User.query.all()
    
    return render_template('admin/manage_users.html', title='Manage Users', 
                          users=users, form=form, search_query=search_query)

# View user profile (admin only)
@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def view_user(user_id):
    if current_user.role != 'admin':
        abort(403)
        
    user = User.query.get_or_404(user_id)
    role_form = UserRoleForm()
    status_form = UserStatusForm()
    
    if request.method == 'GET':
        role_form.role.data = user.role
        status_form.status.data = user.status
    
    return render_template('admin/user_profile.html', title=f'User: {user.username}', 
                          user=user, role_form=role_form, status_form=status_form)

# Change user role (admin only)
@app.route('/change_user_role/<int:user_id>', methods=['POST'])
@login_required
def change_user_role(user_id):
    if current_user.role != 'admin':
        abort(403)
        
    user = User.query.get_or_404(user_id)
    form = UserRoleForm()
    
    if form.validate_on_submit():
        user.role = form.role.data
        db.session.commit()
        flash(f'User role has been updated to {form.role.data}!', 'success')
    
    return redirect(url_for('view_user', user_id=user.user_id))

# Change user status (admin only)
@app.route('/change_user_status/<int:user_id>', methods=['POST'])
@login_required
def change_user_status(user_id):
    if current_user.role != 'admin':
        abort(403)
        
    user = User.query.get_or_404(user_id)
    form = UserStatusForm()
    
    if form.validate_on_submit():
        user.status = form.status.data
        db.session.commit()
        flash(f'User status has been updated to {form.status.data}!', 'success')
    
    return redirect(url_for('view_user', user_id=user.user_id))

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def forbidden_error(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500