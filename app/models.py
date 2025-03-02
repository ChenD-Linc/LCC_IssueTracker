from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    email = db.Column(db.String(320), nullable=False)
    location = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='visitor')
    status = db.Column(db.String(10), nullable=False, default='active')
    profile_image = db.Column(db.String(255), nullable=True, default='default.jpg')
    
    # Relationships
    issues = db.relationship('Issue', backref='reporter', lazy=True)
    comments = db.relationship('Comment', backref='commenter', lazy=True)
    
    def get_id(self):
        return str(self.user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.role}')"

class Issue(db.Model):
    __tablename__ = 'issues'
    issue_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    summary = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(10), nullable=False, default='new')
    date_reported = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    comments = db.relationship('Comment', backref='issue', lazy=True)
    
    def __repr__(self):
        return f"Issue('{self.summary}', '{self.status}')"

class Comment(db.Model):
    __tablename__ = 'comments'
    comment_id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issues.issue_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    comment_text = db.Column(db.Text, nullable=False)
    date_commented = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return f"Comment('{self.comment_text}', '{self.date_commented}')"