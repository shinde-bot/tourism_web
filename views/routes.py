from flask import Blueprint, render_template, request, jsonify
from models import Tour
from extensions import db

views_bp = Blueprint("views", __name__, template_folder="../templates")

# Home page
@views_bp.route("/")
def home():
    tours = Tour.query.order_by(Tour.created_at.desc()).limit(6).all()
    return render_template("home.html", tours=tours)

# Place detail page
@views_bp.route("/place/<int:tour_id>")
def place(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template("place.html", tour=tour)

# Itinerary page
@views_bp.route("/itinerary")
def itinerary():
    tours = Tour.query.order_by(Tour.days).all()
    return render_template("itinerary.html", tours=tours)

# Authentication pages
@views_bp.route("/login")
def login():
    return render_template("login.html")

@views_bp.route("/register")
def register():
    return render_template("register.html")

@views_bp.route("/forgot_password")
def forgot():
    return render_template("forgot_password.html")

@views_bp.route("/reset_password")
def reset():
    return render_template("reset_password.html")

# Dashboard
@views_bp.route("/dashboard")
def dashboard():
    # Dummy dashboard; extend with auth as needed
    return render_template("dashboard.html")

@views_bp.route("/about")
def about():
    # You can pass tours if needed for other sections, or leave empty
    tours = Tour.query.order_by(Tour.created_at.desc()).limit(6).all()
    show_about_only = True  # Flag to show only the About India section
    return render_template("home.html", tours=tours, show_about_only=show_about_only)
