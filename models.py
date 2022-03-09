from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    phonenumber = db.Column(db.String(12), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Order(db.Model):
    id = db.Column('order_id', db.Integer, primary_key=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)