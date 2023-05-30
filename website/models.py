from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import datetime
db = SQLAlchemy()
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    fname = db.Column(db.String(1000))
    lname = db.Column(db.String(1000))


class Upload(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('uploads', lazy=True))
    filename = db.Column(db.String(50))
    data = db.Column(db.LargeBinary)
    upload_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
