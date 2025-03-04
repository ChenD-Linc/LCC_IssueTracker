"""Handles visitor-specific functionality for the LCC Issue Tracker.

This module provides route handlers for the visitor home page and other
visitor-specific features.
"""
from issuetracker import app
from issuetracker import db
from flask import render_template, session, redirect, url_for
from issuetracker.user import role_required

@app.route('/visitor/home')
@role_required(['visitor', 'helper', 'admin'])
def visitor_home():
    """Visitor home page endpoint.
    
    Renders the homepage for visitors, showing a summary of their reported issues.
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
    
    return render_template('visitor_home.html', issues=issues)