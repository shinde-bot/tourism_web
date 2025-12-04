from datetime import datetime
from extensions import db

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    subtitle = db.Column(db.String(200))
    description = db.Column(db.Text, nullable=False)
    days = db.Column(db.Integer, default=3)
    img = db.Column(db.String(200), default="thumb-osaka.jpg")
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(60))
    email = db.Column(db.String(120))
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price_per_night = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(200))

    tour = db.relationship("Tour", backref=db.backref("hotels", lazy=True))
