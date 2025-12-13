from app import create_app
from models import Booking

app = create_app()
with app.app_context():
    bookings = Booking.query.all()
    for b in bookings:
        print(b.id, b.tour_id, b.name, b.email, b.comment)
