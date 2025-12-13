from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# ---------------------------
# Itinerary Model (Optional)
# ---------------------------
class Itinerary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Itinerary {self.title}>"


# ---------------------------
# Tour Model
# ---------------------------
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
    welcome_msg = db.Column(db.String(300), default="Welcome!", nullable=True)

    # Relationship with Hotel
    hotels = db.relationship("Hotel", backref="tour", lazy=True)

class Booking(db.Model):
    __tablename__ = "booking"

    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Optional: Define relationship to Tour
    tour = db.relationship("Tour", backref=db.backref("bookings", lazy=True))

    def __repr__(self):
        return f"<Booking {self.id} - {self.name} - {self.email}>"


# ---------------------------
# Hotel Model
# ---------------------------
class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    price_per_night = db.Column(db.Float, default=0.0)
    location = db.Column(db.String(200), nullable=True)
    img = db.Column(db.String(200), nullable=True)  # Optional image for hotel


# ---------------------------
# Experience Model
# ---------------------------
class Experience(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    short_desc = db.Column(db.String(500), nullable=True)
    long_desc = db.Column(db.Text, nullable=False)
    img = db.Column(db.String(200), nullable=True)  # Image for the experience
    tour_id = db.Column(db.Integer, db.ForeignKey("tour.id"), nullable=True)  # Optional link to a tour

    # Relationship with Tour (optional)
    tour = db.relationship("Tour", backref=db.backref("experiences", lazy=True))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


