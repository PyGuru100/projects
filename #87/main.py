from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
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


@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)
