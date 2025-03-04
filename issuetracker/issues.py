"""Handles functionality related to issues in the LCC Issue Tracker.

This module provides route handlers for creating, viewing, and updating issues.
"""
from issuetracker import app
from issuetracker import db
from flask import render_template, session, redirect, url_for, request, flash
from issuetracker.user import login_required, role_required
from datetime import datetime

@app.route('/issue/new', methods=['GET', 'POST'])
@login_required
def new_issue():
    """New issue creation endpoint.
    
    GET: Renders the new issue form.
    POST: Processes the new issue form submission.
    """
    if request.method == 'POST':
        # Get form data
        summary = request.form['summary']
        description = request.form['description']
        
        # Validate input
        if not summary or len(summary) > 255:
            flash('Summary is required and must be less than 255 characters!', 'error')
            return render_template('issue_form.html', summary=summary, description=description)
        
        if not description:
            flash('Description is required!', 'error')
            return render_template('issue_form.html', summary=summary, description=description)
        
        # Create new issue
        with db.get_cursor() as cursor:
            cursor.execute('''
                          INSERT INTO issues (user_id, summary, description, status)
                          VALUES (%s, %s, %s, %s);
                          ''',
                          (session['user_id'], summary, description, 'new'))
            
            # Get the newly created issue ID
            cursor.execute('SELECT LAST_INSERT_ID() AS issue_id')
            issue_id = cursor.fetchone()['issue_id']
        
        flash('Issue reported successfully!', 'success')
        return redirect(url_for('view_issue', issue_id=issue_id))
    
    # GET request
    return render_template('issue_form.html')

@app.route('/issue/<int:issue_id>', methods=['GET'])
@login_required
def view_issue(issue_id):
    """Issue detail view endpoint.
    
    Renders a page showing details of a specific issue and its comments.
    """
    # Get issue details
    with db.get_cursor() as cursor:
        cursor.execute('''
                      SELECT i.issue_id, i.summary, i.description, i.status, i.created_at,
                             u.user_id, u.username, u.first_name, u.last_name, u.profile_image
                      FROM issues i
                      INNER JOIN users u ON i.user_id = u.user_id
                      WHERE i.issue_id = %s;
                      ''',
                      (issue_id,))
        issue = cursor.fetchone()
        
        if not issue:
            flash('Issue not found!', 'error')
            return redirect(url_for('root'))
        
        # Check access rights
        user_role = session.get('role')
        user_id = session.get('user_id')
        
        # Only allow visitors to view their own issues
        if user_role == 'visitor' and issue['user_id'] != user_id:
            return render_template('access_denied.html'), 403
        
        # Get comments on this issue
        cursor.execute('''
                      SELECT c.comment_id, c.content, c.created_at,
                             u.user_id, u.username, u.first_name, u.last_name, 
                             u.profile_image, u.role
                      FROM comments c
                      INNER JOIN users u ON c.user_id = u.user_id
                      WHERE c.issue_id = %s
                      ORDER BY c.created_at;
                      ''',
                      (issue_id,))
        comments = cursor.fetchall()
    
    return render_template('issue_detail.html', 
                          issue=issue, 
                          comments=comments)

@app.route('/issue/<int:issue_id>/comment', methods=['POST'])
@login_required
def add_comment(issue_id):
    """Add comment to issue endpoint.
    
    Processes the comment form submission and redirects back to the issue detail page.
    """
    # Get form data
    content = request.form['content']
    
    # Validate input
    if not content:
        flash('Comment cannot be empty!', 'error')
        return redirect(url_for('view_issue', issue_id=issue_id))
    
    # Get issue details to check access and current status
    with db.get_cursor() as cursor:
        cursor.execute('''
                      SELECT user_id, status
                      FROM issues
                      WHERE issue_id = %s;
                      ''',
                      (issue_id,))
        issue = cursor.fetchone()
        
        if not issue:
            flash('Issue not found!', 'error')
            return redirect(url_for('root'))
        
        # Check access rights
        user_role = session.get('role')
        user_id = session.get('user_id')
        
        # Only allow visitors to comment on their own issues
        if user_role == 'visitor' and issue['user_id'] != user_id:
            return render_template('access_denied.html'), 403
        
        # Add the comment
        cursor.execute('''
                      INSERT INTO comments (issue_id, user_id, content)
                      VALUES (%s, %s, %s);
                      ''',
                      (issue_id, user_id, content))
        
        # If helper/admin comments on new, stalled, or resolved issue, change status to open
        if user_role in ['helper', 'admin'] and issue['status'] in ['new', 'stalled', 'resolved']:
            cursor.execute('''
                          UPDATE issues
                          SET status = 'open'
                          WHERE issue_id = %s;
                          ''',
                          (issue_id,))
            flash('Comment added and issue opened for investigation!', 'success')
        else:
            flash('Comment added successfully!', 'success')
    
    return redirect(url_for('view_issue', issue_id=issue_id))

@app.route('/issues', methods=['GET'])
@login_required
def my_issues():
    """My issues list endpoint.
    
    Renders a page showing all issues reported by the current user.
    """
    # Get user's reported issues
    with db.get_cursor() as cursor:
        cursor.execute('''
                      SELECT i.issue_id, i.summary, i.status, i.created_at,
                             COUNT(c.comment_id) AS comment_count
                      FROM issues i
                      LEFT JOIN comments c ON i.issue_id = c.issue_id
                      WHERE i.user_id = %s
                      GROUP BY i.issue_id
                      ORDER BY i.created_at DESC;
                      ''',
                      (session['user_id'],))
        issues = cursor.fetchall()
    
    return render_template('my_issues.html', issues=issues)

@app.route('/all-issues', methods=['GET'])
@role_required(['helper', 'admin'])
def all_issues():
    """All issues list endpoint for helpers and admins.
    
    Renders a page showing all active issues (non-resolved).
    """
    # Get filter parameters
    status_filter = request.args.get('status', 'active')
    
    if status_filter == 'all':
        status_clause = ""
    elif status_filter == 'active':
        status_clause = "WHERE i.status IN ('new', 'open', 'stalled')"
    elif status_filter in ['new', 'open', 'stalled', 'resolved']:
        status_clause = f"WHERE i.status = '{status_filter}'"
    else:
        status_clause = "WHERE i.status IN ('new', 'open', 'stalled')"
    
    # Get issues based on filter
    with db.get_cursor() as cursor:
        cursor.execute(f'''
                      SELECT i.issue_id, i.summary, i.status, i.created_at,
                             u.username, u.first_name, u.last_name,
                             COUNT(c.comment_id) AS comment_count
                      FROM issues i
                      INNER JOIN users u ON i.user_id = u.user_id
                      LEFT JOIN comments c ON i.issue_id = c.issue_id
                      {status_clause}
                      GROUP BY i.issue_id
                      ORDER BY 
                          CASE 
                              WHEN i.status = 'new' THEN 1
                              WHEN i.status = 'open' THEN 2
                              WHEN i.status = 'stalled' THEN 3
                              WHEN i.status = 'resolved' THEN 4
                          END,
                          i.created_at DESC;
                      ''')
        issues = cursor.fetchall()
    
    return render_template('all_issues.html', 
                          issues=issues,
                          status_filter=status_filter)