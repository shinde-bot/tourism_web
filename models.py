from datetime import datetime
from extensions import db

class Tour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    subtitle = db.Column(db.String(200), nullable=True)
    description = db.Column(db.Text, nullable=False)
    days = db.Column(db.Integer, default=3)
    img = db.Column(db.String(200), default="thumb-osaka.jpg", nullable=True)
    price = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Extended fields
    highlights = db.Column(db.PickleType, default=[])
    places_to_visit = db.Column(db.PickleType, default=[])
    cuisine = db.Column(db.PickleType, default=[])
    history = db.Column(db.Text, nullable=True)
    gallery = db.Column(db.PickleType, default=[])
    welcome_msg = db.Column(db.String(300), default="Welcome!", nullable=True)  # New field

    # Relationship with Hotel
    hotels = db.relationship("Hotel", backref="tour", lazy=True)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(60), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price_per_night = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(200), nullable=True)
    img = db.Column(db.String(200), nullable=True)  # Optional image for hotel
