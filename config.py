import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key_replace_in_production')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'mysql+pymysql://root:password@localhost/lcc_issue_tracker')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app/static/profile_pics')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload