from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.getcwd()}/cafes.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    map_url = db.Column(db.String, nullable=False)
    img_url = db.Column(db.String, nullable=True)
    location = db.Column(db.String, nullable=True)
    has_sockets = db.Column(db.Boolean, nullable=True)
    has_wifi = db.Column(db.Boolean, nullable=True)
    has_toilet = db.Column(db.Boolean, nullable=True)
    can_take_calls = db.Column(db.Boolean, nullable=True)
    seats = db.Column(db.String, nullable=True)
    coffee_price = db.Column(db.String, nullable=True)


db.create_all()
q = Cafe.query
print(q.column_descriptions)
