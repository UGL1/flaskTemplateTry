# Here are all the ORM
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

from app import app

# add database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'

# init the db
db = SQLAlchemy(app)


# ORM definitions

# User database
class UserDB(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(40), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, user_name, first_name, last_name, email, password):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)

    def password_match(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

#u = UserDB(user_name="UGLi",first_name="Fred",last_name="Leleu",email="ugli@mailo.com",password="salut")

