from flask import Blueprint, render_template, request
from __init__ import db

admin_blueprint = Blueprint('admin', __name__)

@admin_blueprint.route('/manage_users', methods=['GET'])
def manage_users():
    search_query = request.args.get('search', '')
    if search_query:
        users = db.execute(f"SELECT * FROM users WHERE username LIKE '%{search_query}%' OR first_name LIKE '%{search_query}%' OR last_name LIKE '%{search_query}%'").fetchall()
    else:
        users = db.execute("SELECT * FROM users").fetchall()
    return render_template('admin/manage_users.html', users=users, search_query=search_query)

@admin_blueprint.route('/change_status/<int:user_id>', methods=['POST'])
def change_status(user_id):
    current_status = db.execute(f"SELECT status FROM users WHERE user_id = {user_id}").fetchone()[0]
    new_status = 0 if current_status == 1 else 1
    db.execute(f"UPDATE users SET status = {new_status} WHERE user_id = {user_id}")
    db.commit()
    return redirect(url_for('admin.manage_users'))