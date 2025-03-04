"""Handles admin-specific functionality for the LCC Issue Tracker.

This module provides route handlers for the admin home page and other
admin-specific features like user management.
"""
from issuetracker import app
from issuetracker import db
from flask import render_template, session, redirect, url_for, request, flash
from issuetracker.user import role_required
import math

@app.route('/admin/home')
@role_required(['admin'])
def admin_home():
    """Admin home page endpoint.
    
    Renders the homepage for administrators, showing a dashboard with
    key statistics and recent activity.
    """
    # Get stats for dashboard
    with db.get_cursor() as cursor:
        # Count active users by role
        cursor.execute('''
                      SELECT 
                          SUM(CASE WHEN role = 'visitor' THEN 1 ELSE 0 END) AS visitor_count,
                          SUM(CASE WHEN role = 'helper' THEN 1 ELSE 0 END) AS helper_count,
                          SUM(CASE WHEN role = 'admin' THEN 1 ELSE 0 END) AS admin_count
                      FROM users
                      WHERE status = 'active';
                      ''')
        user_stats = cursor.fetchone()
        
        # Count issues by status
        cursor.execute('''
                      SELECT 
                          SUM(CASE WHEN status = 'new' THEN 1 ELSE 0 END) AS new_count,
                          SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) AS open_count,
                          SUM(CASE WHEN status = 'stalled' THEN 1 ELSE 0 END) AS stalled_count,
                          SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) AS resolved_count
                      FROM issues;
                      ''')
        issue_stats = cursor.fetchone()
        
        # Get recent activity (last 5 comments)
        cursor.execute('''
                      SELECT c.content, c.created_at, 
                             u.username, u.role, u.profile_image,
                             i.issue_id, i.summary
                      FROM comments c
                      INNER JOIN users u ON c.user_id = u.user_id
                      INNER JOIN issues i ON c.issue_id = i.issue_id
                      ORDER BY c.created_at DESC
                      LIMIT 5;
                      ''')
        recent_activity = cursor.fetchall()
    
    return render_template('admin_home.html', 
                          user_stats=user_stats,
                          issue_stats=issue_stats,
                          recent_activity=recent_activity)

@app.route('/admin/users', methods=['GET'])
@role_required(['admin'])
def manage_users():
    """User management page endpoint.
    
    Renders a page showing all users with options to search, change status, or change role.
    """
    # Get search parameters
    search_term = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Build search query
    base_query = '''
                FROM users
                WHERE (username LIKE %s OR
                       first_name LIKE %s OR
                       last_name LIKE %s)
                '''
    search_param = f'%{search_term}%'
    
    # Get total count for pagination
    with db.get_cursor() as cursor:
        cursor.execute(f'SELECT COUNT(*) AS count {base_query}',
                      (search_param, search_param, search_param))
        total_users = cursor.fetchone()['count']
    
    # Calculate total pages
    total_pages = math.ceil(total_users / per_page)
    
    # Get users for current page
    with db.get_cursor() as cursor:
        cursor.execute(f'''
                      SELECT user_id, username, email, first_name, last_name,
                             location, profile_image, role, status
                      {base_query}
                      ORDER BY username
                      LIMIT %s OFFSET %s;
                      ''',
                      (search_param, search_param, search_param, per_page, offset))
        users = cursor.fetchall()
    
    return render_template('manage_users.html',
                          users=users,
                          search_term=search_term,
                          page=page,
                          total_pages=total_pages)

@app.route('/admin/user/<int:user_id>', methods=['GET'])
@role_required(['admin'])
def view_user(user_id):
    """User profile view endpoint for admins.
    
    Renders a page showing details of a specific user.
    """
    # Get user details
    with db.get_cursor() as cursor:
        cursor.execute('''
                      SELECT user_id, username, email, first_name, last_name,
                             location, profile_image, role, status
                      FROM users
                      WHERE user_id = %s;
                      ''',
                      (user_id,))
        user = cursor.fetchone()
        
        if not user:
            flash('User not found!', 'error')
            return redirect(url_for('manage_users'))
        
        # Get user's reported issues
        cursor.execute('''
                      SELECT issue_id, summary, status, created_at
                      FROM issues
                      WHERE user_id = %s
                      ORDER BY created_at DESC;
                      ''',
                      (user_id,))
        user_issues = cursor.fetchall()
    
    return render_template('view_user.html', user=user, user_issues=user_issues)

@app.route('/admin/user/<int:user_id>/status', methods=['POST'])
@role_required(['admin'])
def change_user_status(user_id):
    """Change user status endpoint.
    
    Updates the status of a user (active/inactive).
    """
    new_status = request.form['status']
    
    # Validate status
    if new_status not in ['active', 'inactive']:
        flash('Invalid status!', 'error')
        return redirect(url_for('view_user', user_id=user_id))
    
    # Prevent self-deactivation
    if user_id == session['user_id'] and new_status == 'inactive':
        flash('You cannot deactivate your own account!', 'error')
        return redirect(url_for('view_user', user_id=user_id))
    
    # Update user status
    with db.get_cursor() as cursor:
        cursor.execute('UPDATE users SET status = %s WHERE user_id = %s',
                      (new_status, user_id))
    
    flash(f'User status updated to {new_status}!', 'success')
    return redirect(url_for('view_user', user_id=user_id))

@app.route('/admin/user/<int:user_id>/role', methods=['POST'])
@role_required(['admin'])
def change_user_role(user_id):
    """Change user role endpoint.
    
    Updates the role of a user (visitor/helper/admin).
    """
    new_role = request.form['role']
    
    # Validate role
    if new_role not in ['visitor', 'helper', 'admin']:
        flash('Invalid role!', 'error')
        return redirect(url_for('view_user', user_id=user_id))
    
    # Prevent last admin removal
    if user_id == session['user_id'] and new_role != 'admin':
        # Check if this is the last admin
        with db.get_cursor() as cursor:
            cursor.execute('SELECT COUNT(*) AS count FROM users WHERE role = "admin"')
            admin_count = cursor.fetchone()['count']
            
            if admin_count <= 1:
                flash('You cannot change your role as you are the last administrator!', 'error')
                return redirect(url_for('view_user', user_id=user_id))
    
    # Update user role
    with db.get_cursor() as cursor:
        cursor.execute('UPDATE users SET role = %s WHERE user_id = %s',
                      (new_role, user_id))
    
    flash(f'User role updated to {new_role}!', 'success')
    return redirect(url_for('view_user', user_id=user_id))