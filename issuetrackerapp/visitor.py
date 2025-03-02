from flask import Blueprint, render_template, request
from __init__ import db

visitor_blueprint = Blueprint('visitor', __name__)

@visitor_blueprint.route('/report_issue', methods=['GET', 'POST'])
def report_issue():
    if request.method == 'POST':
        # Logic to report an issue
        pass
    return render_template('visitor/report_issue.html')

@visitor_blueprint.route('/view_reports', methods=['GET'])
def view_reports():
    # Logic to view own reports
    return render_template('visitor/view_reports.html')