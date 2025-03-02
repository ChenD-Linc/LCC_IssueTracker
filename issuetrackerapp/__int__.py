from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@localhost/your_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from admin import admin_blueprint
from helper import helper_blueprint
from visitor import visitor_blueprint

app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(helper_blueprint, url_prefix='/helper')
app.register_blueprint(visitor_blueprint, url_prefix='/visitor')