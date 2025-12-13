from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_mail import Message
from extensions import db, mail
from models import Booking, Tour, User
from datetime import datetime
from forms import RegisterForm, LoginForm

views_bp = Blueprint("views", __name__, template_folder="../templates")

# ----------------------------
# Home Page
# ----------------------------
@views_bp.route("/")
def home():
    tours = Tour.query.order_by(Tour.created_at.desc()).limit(6).all()
    return render_template("home.html", tours=tours)

# ----------------------------
# Place / Tour Detail
# ----------------------------
@views_bp.route("/place/<int:tour_id>")
def place(tour_id):
    tour = Tour.query.get_or_404(tour_id)
    return render_template("place.html", tour=tour)

# ----------------------------
# Itinerary Page
# ----------------------------
@views_bp.route("/itinerary")
def itinerary():
    tours = Tour.query.order_by(Tour.days).all()
    return render_template("itinerary.html", tours=tours)

# ----------------------------
# About Page
# ----------------------------
@views_bp.route("/about")
def about():
    tours = Tour.query.order_by(Tour.created_at.desc()).limit(6).all()
    show_about_only = True
    return render_template("home.html", tours=tours, show_about_only=show_about_only)

# ----------------------------
# Submit Booking / Itinerary
# ----------------------------
@views_bp.route("/submit", methods=["POST"])
def submit():
    tour_id = request.form.get("tour_id")

    if not tour_id:
        flash("Please select a tour", "danger")
        return redirect(url_for("views.home"))

    booking = Booking(
        tour_id=tour_id,
        name=request.form.get("name"),
        email=request.form.get("email"),
        phone=request.form.get("phone"),
        comment=request.form.get("comment"),
        created_at=datetime.utcnow()
    )

    db.session.add(booking)
    db.session.commit()

    # Send itinerary email only to the submitting user
    tour = Tour.query.get(tour_id)
    msg = Message(
        subject=f"Your Itinerary for {tour.title}",
        sender=("India Tours", "YOUR_GMAIL@gmail.com"),  # replace with your sender email
        recipients=[booking.email]
    )
    msg.body = f"""
Hello {booking.name},

Thank you for choosing India Tours!

Tour: {tour.title}
Duration: {tour.days} days
Description: {tour.description}
Message: {booking.comment}

We will contact you soon with full details.

Regards,
India Tours
"""
    mail.send(msg)

    flash("Your itinerary has been sent to your email!", "success")
    return redirect(url_for("views.home"))

# ----------------------------
# Login
# ----------------------------
@views_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session["user_id"] = user.id
            flash("Login successful!", "success")
            return redirect(url_for("views.dashboard"))
        else:
            flash("Invalid email or password", "danger")
            return redirect(url_for("views.login"))
    return render_template("login.html", form=form)

# ----------------------------
# Register
# ----------------------------
@views_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Check if user/email already exists
        if User.query.filter_by(email=form.email.data).first():
            flash("Email is already registered. Please login.", "danger")
            return redirect(url_for("views.login"))

        # Create new user
        user = User(
            username=form.username.data,
            email=form.email.data
        )
        user.set_password(form.password.data)  # hash password
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully! Please login.", "success")
        return redirect(url_for("views.login"))

    return render_template("register.html", form=form)

# ----------------------------
# Dashboard
# ----------------------------
@views_bp.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        flash("Please login first!", "warning")
        return redirect(url_for("views.login"))
    user = User.query.get(session["user_id"])
    return render_template("dashboard.html", user=user)
