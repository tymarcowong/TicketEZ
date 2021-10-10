from . import db
from datetime import datetime
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    contactNumber = db.Column(db.Integer(20), index=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    comments = db.relationship('Comment', backref='user')


class Booking(db.Model):
    __tablename__ = 'booking'
    id = db.Column(db.Integer, primary_key=True)
    num_tickets = db.Column(db.Integer, index=True, nullable=False)
    price = db.Column(db.Integer, index=True, nullable=False)
    tickets_available = db.Column(db.Integer, index=True, nullable=False)
    booking_status = db.Column(db.String(100), index=True, nullable=False)
    orderID = db.Column(db.Integer, index=True, unique=True, nullable=False)

    user = db.relationship('User', backref='booking')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(400))
    posted_at = db.Column(db.DateTime, default=datetime.now())

    # foreign keys
    event_id = db.Column(db.Integer, db.ForeignKey('event.event_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Event(db.Model):
    __tablename__ = 'event'
    event_id = db.Column(db.Integer, primary_key=True)
    event_status = db.Column(db.String(20), index=True, nullable=False)
    event_name = db.Column(db.String(80), index=True, nullable=False)
    event_genre = db.Column(db.String(80), index=True, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())
    location = db.Column(db.String(200), index=True, nullable=False)
    google_map = db.Column(db.String(500), index=True, nullable=False)
    description = db.Column(db.String(500), index=True, nullable=False)
    image = db.Column(db.String(400), index=True, nullable=False)
    price = db.Column(db.Integer(5), index=True, nullable=False)

    comments = db.relationship('Comment', backref='event')