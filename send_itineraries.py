from app import create_app
from extensions import db, mail
from models import Booking, Tour
from flask_mail import Message

app = create_app()

with app.app_context():
    bookings = Booking.query.all()

    for b in bookings:
        tour = Tour.query.get(b.tour_id)
        if not tour:
            continue

        msg = Message(
            subject=f"Your Itinerary for {tour.title}",
            sender=app.config["MAIL_USERNAME"],  # <-- your Gmail sender
            recipients=[b.email]                 # <-- user's email from DB
        )

        msg.body = f"""
Hi {b.name},

Thank you for requesting the itinerary for {tour.title}.

Tour Details:
- Title: {tour.title}
- Subtitle: {tour.subtitle}
- Description: {tour.description}
- Days: {tour.days}
- Places to Visit: {', '.join(tour.places_to_visit)}

We hope you enjoy your trip!

Best regards,
India Tours Team
        """

        mail.send(msg)
        print(f"Sent itinerary to {b.email}")
