from flask import Blueprint, render_template, request
from __init__ import db

helper_blueprint = Blueprint('helper', __name__)

@helper_blueprint.route('/view_issues', methods=['GET'])
def view_issues():
    # Logic to view issues
    return render_template('helper/view_issues.html')

@helper_blueprint.route('/update_issue/<int:issue_id>', methods=['POST'])
def update_issue(issue_id):
    # Logic to update issue status
    return redirect(url_for('helper.view_issues'))