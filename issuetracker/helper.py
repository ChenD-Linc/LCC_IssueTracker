"""Handles helper-specific functionality for the LCC Issue Tracker.

This module provides route handlers for the helper home page and other
helper-specific features.
"""
from issuetracker import app
from issuetracker import db
from flask import render_template, session, redirect, url_for, request, flash
from issuetracker.user import role_required
import math

@app.route('/helper/home')
@role_required(['helper', 'admin'])
def helper_home():
    """Helper home page endpoint.
    
    Renders the homepage for helpers, showing a list of active issues that need attention.
    """
    # Get active issues (new, open, stalled)
    with db.get_cursor() as cursor:
        cursor.execute('''
                      SELECT i.issue_id, i.summary, i.status, i.created_at,
                             u.username, u.first_name, u.last_name,
                             COUNT(c.comment_id) AS comment_count
                      FROM issues i
                      INNER JOIN users u ON i.user_id = u.user_id
                      LEFT JOIN comments c ON i.issue_id = c.issue_id
                      WHERE i.status IN ('new', 'open', 'stalled')
                      GROUP BY i.issue_id
                      ORDER BY 
                          CASE 
                              WHEN i.status = 'new' THEN 1
                              WHEN i.status = 'open' THEN 2
                              WHEN i.status = 'stalled' THEN 3
                          END,
                          i.created_at DESC;
                      ''')
        active_issues = cursor.fetchall()
    
    return render_template('helper_home.html', active_issues=active_issues)

@app.route('/helper/resolved')
@role_required(['helper', 'admin'])
def resolved_issues():
    """Resolved issues page endpoint.
    
    Renders a page showing all resolved issues.
    """
    # Get page number from query parameter (default to 1)
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    
    # Get total number of resolved issues
    with db.get_cursor() as cursor:
        cursor.execute('SELECT COUNT(*) AS count FROM issues WHERE status = "resolved"')
        total_issues = cursor.fetchone()['count']
    
    # Calculate total pages
    total_pages = math.ceil(total_issues / per_page)
    
    # Get resolved issues for current page
    with db.get_cursor() as cursor:
        cursor.execute('''
                      SELECT i.issue_id, i.summary, i.created_at,
                             u.username, u.first_name, u.last_name,
                             COUNT(c.comment_id) AS comment_count
                      FROM issues i
                      INNER JOIN users u ON i.user_id = u.user_id
                      LEFT JOIN comments c ON i.issue_id = c.issue_id
                      WHERE i.status = 'resolved'
                      GROUP BY i.issue_id
                      ORDER BY i.created_at DESC
                      LIMIT %s OFFSET %s;
                      ''',
                      (per_page, offset))
        resolved_issues = cursor.fetchall()
    
    return render_template('resolved_issues.html', 
                          resolved_issues=resolved_issues,
                          page=page,
                          total_pages=total_pages)

@app.route('/helper/update_status/<int:issue_id>', methods=['POST'])
@role_required(['helper', 'admin'])
def update_status(issue_id):
    """Update issue status endpoint.
    
    Updates the status of an issue and redirects back to the referring page.
    """
    new_status = request.form['status']
    
    # Validate new status
    if new_status not in ['new', 'open', 'stalled', 'resolved']:
        flash('Invalid status!', 'error')
        return redirect(url_for('view_issue', issue_id=issue_id))
    
    # Update issue status
    with db.get_cursor() as cursor:
        cursor.execute('UPDATE issues SET status = %s WHERE issue_id = %s',
                      (new_status, issue_id))
    
    flash(f'Issue status updated to {new_status}!', 'success')
    
    # Redirect back to referring page
    return redirect(request.referrer or url_for('helper_home'))