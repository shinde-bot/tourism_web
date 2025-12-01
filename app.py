import logging
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, logout_user, login_required, current_user, UserMixin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail, Message

from config import Config
from models import db, User
from forms import LoginForm, RegistrationForm, ForgotPasswordForm

# --- App setup ---
app = Flask(__name__)
app.config.from_object(Config)

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

# Extensions
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Flask-Limiter
limiter = Limiter(app, key_func=get_remote_address, default_limits=[])

# Flask-Mail config (replace with real values)
app.config.update(
    MAIL_SERVER='smtp.example.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='your-email@example.com',
    MAIL_PASSWORD='your-email-password'
)
mail = Mail(app)

# --- User wrapper for Flask-Login ---
class AuthUser(UserMixin):
    def __init__(self, user):
        self._user = user

    def get_id(self):
        return str(self._user.id)

    @property
    def username(self):
        return self._user.username

    @property
    def model(self):
        return self._user

@login_manager.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    if user:
        return AuthUser(user)
    return None

# --- Create DB tables once ---
@app.before_request
def create_tables_once():
    if not hasattr(app, "_tables_created"):
        with app.app_context():
            db.create_all()
        app._tables_created = True

# --- India tourism data ---
PLACES = [
    {"id":"taj", "name":"Taj Mahal", "region":"Agra (Uttar Pradesh)",
     "description":"An immense white-marble mausoleum built by Mughal emperor Shah Jahan.",
     "image":"taj-mahal.jpg"},
    {"id":"amber", "name":"Amber Fort", "region":"Jaipur (Rajasthan)",
     "description":"A hilltop palace-fort near Jaipur known for mirror-work Sheesh Mahal.",
     "image":"amber-fort.jpg"},
    {"id":"varanasi", "name":"Varanasi Ghats", "region":"Varanasi (Uttar Pradesh)",
     "description":"Historic stepped riverfronts on the Ganges for rituals and sunrise boat rides.",
     "image":"varanasi-ghats.jpg"},
    {"id":"kerala", "name":"Kerala Backwaters", "region":"Kerala",
     "description":"Scenic lagoons and canals, houseboat cruises through palm-fringed waterways.",
     "image":"kerala-houseboat.jpg"},
    {"id":"pangong", "name":"Pangong Lake", "region":"Ladakh",
     "description":"High-altitude, color-changing lake in eastern Ladakh.",
     "image":"pangong.jpg"},
    {"id":"gateway", "name":"Gateway of India", "region":"Mumbai (Maharashtra)",
     "description":"Iconic arch monument on the Mumbai waterfront built in early 20th century.",
     "image":"gateway-mumbai.jpg"}
]

ITINERARIES = {
    "north_7": {
        "title":"7-day North India Highlights",
        "days":[
            "Day 1: Delhi — India Gate, Connaught Place",
            "Day 2: Agra — Taj Mahal + Agra Fort",
            "Day 3: Fatehpur Sikri then to Jaipur",
            "Day 4: Jaipur — Amber Fort, City Palace",
            "Day 5: Jaipur to Varanasi (overnight train/flight)",
            "Day 6: Varanasi — Ganges sunrise boat, temples, evening aarti",
            "Day 7: Return to Delhi / depart"
        ]
    },
    "kerala_7": {
        "title":"7-day Kerala Relax & Backwaters",
        "days":[
            "Day 1: Kochi — Fort Kochi, Chinese fishing nets",
            "Day 2: Munnar — tea gardens",
            "Day 3: Munnar to Thekkady — spice plantations, wildlife",
            "Day 4-5: Alleppey — overnight houseboat on backwaters",
            "Day 6: Kovalam — beach time",
            "Day 7: Trivandrum — departure"
        ]
    },
    "rajasthan_5": {
        "title":"5-day Rajasthan Quick Tour",
        "days":[
            "Day 1: Jaipur — Amber Fort + bazaars",
            "Day 2: Jaipur — Jal Mahal / City Palace",
            "Day 3: Pushkar / Ajmer day trip",
            "Day 4: Jodhpur (optional)",
            "Day 5: Return or extend to Udaipur"
        ]
    }
}

# --- Routes ---
@app.route("/")
def home():
    # Pass both places and itineraries to template
    return render_template("home.html", places=PLACES, itineraries=ITINERARIES)

@app.route("/place/<place_id>")
def place_detail(place_id):
    place = next((p for p in PLACES if p["id"] == place_id), None)
    if not place:
        flash("Place not found", "danger")
        return redirect(url_for("home"))
    return render_template("place.html", place=place)

@app.route("/itinerary")
def itinerary():
    return render_template("itinerary.html", itineraries=ITINERARIES)

# --- Authentication routes (login/register/forgot-password) ---
@app.route("/login", methods=["GET", "POST"])
@limiter.limit("5 per minute")
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if not user:
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        if user.is_locked():
            flash("Account locked due to too many failed attempts.", "danger")
            return render_template("login.html", form=form)

        if bcrypt.check_password_hash(user.password_hash, password):
            user.failed_attempts = 0
            user.locked_until = None
            db.session.commit()
            login_user(AuthUser(user))
            next_page = request.args.get("next") or url_for("dashboard")
            return redirect(next_page)
        else:
            user.failed_attempts = (user.failed_attempts or 0) + 1
            if user.failed_attempts >= 5:
                user.lock(minutes=15)
            db.session.commit()
            flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(
            (User.username == form.username.data.strip()) |
            (User.email == form.email.data.strip())
        ).first()
        if existing_user:
            flash("Username or email already exists.", "warning")
            return render_template("register.html", form=form)

        pw_hash = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        new_user = User(username=form.username.data.strip(),
                        email=form.email.data.strip(),
                        password_hash=pw_hash)
        db.session.add(new_user)
        db.session.commit()
        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("login"))
    return render_template("register.html", form=form)

@app.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    form = ForgotPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.strip()
        user = User.query.filter_by(email=email).first()
        if user:
            token = "dummy-token"  # TODO: generate real token
            msg = Message(
                subject="Password Reset Request",
                sender="no-reply@example.com",
                recipients=[email]
            )
            msg.body = f"Hello {user.username},\nClick to reset: http://127.0.0.1:5000/reset-password/{token}"
            mail.send(msg)
            flash("Password reset instructions sent.", "info")
        else:
            flash("No account found with that email.", "warning")
        return redirect(url_for("login"))
    return render_template("forgot_password.html", form=form)

@app.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    return render_template("reset_password.html", token=token)

@app.route("/dashboard")
@login_required
def dashboard():
    username = getattr(current_user, "username", "User")
    return render_template("dashboard.html", username=username)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))

@app.route("/create_user", methods=["POST"])
def create_user():
    data = request.get_json(silent=True) or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    if not all([username, email, password]):
        return jsonify({"error": "invalid"}), 400
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "exists"}), 409
    pw_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    u = User(username=username, email=email, password_hash=pw_hash)
    db.session.add(u)
    db.session.commit()
    return jsonify({"status": "created"}), 201

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
