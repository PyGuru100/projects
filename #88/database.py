from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os

temp = '/'.join(os.getcwd().replace("\\", '/').split('/')[1:])

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:////{temp}/new.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'TEMP BULLSHIT AH1235412'
db = SQLAlchemy(app)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(), nullable=False)
    tasks_do = db.Column(db.String())
    tasks_done = db.Column(db.String())
    tasks_doing = db.Column(db.String())
    undo_data = db.Column(db.String())


print([user.email for user in User.query.filter_by(email='ass@poop.com')])
