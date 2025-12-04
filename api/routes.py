from flask import Blueprint, jsonify, request
from models import Tour, Booking
from extensions import db

api_bp = Blueprint("api", __name__)

@api_bp.route("/tours", methods=["GET"])
def list_tours():
    tours = Tour.query.order_by(Tour.created_at.desc()).all()
    data = [{
        "id": t.id,
        "title": t.title,
        "subtitle": t.subtitle,
        "description": t.description,
        "days": t.days,
        "img": t.img,
        "price": t.price
    } for t in tours]
    return jsonify(data), 200

@api_bp.route("/tours/<int:tour_id>", methods=["GET"])
def get_tour(tour_id):
    t = Tour.query.get_or_404(tour_id)
    data = {
        "id": t.id, "title": t.title, "subtitle": t.subtitle,
        "description": t.description, "days": t.days, "img": t.img, "price": t.price
    }
    return jsonify(data), 200

@api_bp.route("/book", methods=["POST"])
def create_booking():
    payload = request.get_json() or {}
    required = ["tour_id", "name"]
    if not all(k in payload for k in required):
        return jsonify({"error":"Missing fields (tour_id, name required)"}), 400
    tour = Tour.query.get(payload["tour_id"])
    if not tour:
        return jsonify({"error":"Tour not found"}), 404
    b = Booking(
        tour_id=payload["tour_id"],
        name=payload["name"],
        phone=payload.get("phone"),
        email=payload.get("email"),
        comment=payload.get("comment")
    )
    db.session.add(b)
    db.session.commit()
    return jsonify({"id": b.id, "message":"Booked"}), 201

@api_bp.route("/send-itinerary", methods=["POST"])
def send_itinerary():
    data = request.get_json()
    tour_id = data.get("tour_id")
    email = data.get("email")
    tour = Tour.query.get(tour_id)
    if not tour:
        return jsonify({"error":"Tour not found"}), 404
    try:
        msg = Message(
            subject=f"Your Itinerary: {tour.title}",
            sender="your_email@gmail.com",
            recipients=[email],
            html=f"<h2>{tour.title} - {tour.days} Days</h2><p>{tour.description}</p><p>Price: €{tour.price}</p>"
        )
        mail.send(msg)
        return jsonify({"message":"Itinerary sent successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

