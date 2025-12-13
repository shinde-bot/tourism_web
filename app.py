from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from extensions import db, mail
from flask_cors import CORS
from models import Experience, Tour, Booking  # Import Booking model

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ----------------------------
    # Configuration
    # ----------------------------
    app.config.from_object(Config)
    # Ensure SQLite database URI is set
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///india_tours.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = Config.SECRET_KEY  # Needed for flash messages

    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Import and register blueprints
        from api.routes import api_bp
        from views.routes import views_bp

        app.register_blueprint(api_bp, url_prefix="/api")
        app.register_blueprint(views_bp)

        # ----------------------------
        # Routes for Experiences
        # ----------------------------
        # List all experiences
        @app.route("/experiences")
        def experiences():
            experiences_list = Experience.query.all()
            return render_template("experiences.html", experiences=experiences_list)

        # Single experience detail page
        @app.route("/experience/<int:exp_id>")
        def experience_detail(exp_id):
            e = Experience.query.get_or_404(exp_id)
            return render_template("experience_detail.html", e=e)

        # Experiences filtered by tour
        @app.route("/tour/<int:tour_id>/experiences")
        def experiences_by_tour(tour_id):
            tour = Tour.query.get_or_404(tour_id)
            experiences_list = tour.experiences
            return render_template("experiences.html", experiences=experiences_list)

        # ----------------------------
        # Booking Form Submission
        # ----------------------------
        @app.route("/submit", methods=["POST"])
        def submit():
            tour_id = request.form.get("tour_id")
            name = request.form.get("name")
            email = request.form.get("email")
            phone = request.form.get("phone")
            comment = request.form.get("comment")

            # Validate tour selection
            if not tour_id:
                flash("Please select a tour before submitting.", "danger")
                return redirect(url_for("views.home"))

            # Create new booking
            booking = Booking(
                tour_id=int(tour_id),
                name=name,
                email=email,
                phone=phone,
                comment=comment
            )
            db.session.add(booking)
            db.session.commit()

            flash("Your itinerary request has been submitted successfully!", "success")
            return redirect(url_for("views.home"))

        # Create database tables if they don't exist
        db.create_all()

    return app

if __name__ == "__main__":
    create_app().run(debug=True)
