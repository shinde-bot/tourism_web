from flask import Flask
from config import Config
from extensions import db
from flask_cors import CORS
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    
    # Enable CORS for API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        # Import blueprints
        from api.routes import api_bp
        from views.routes import views_bp

        # Register blueprints
        app.register_blueprint(api_bp, url_prefix="/api")
        app.register_blueprint(views_bp)

        # ----------------------------
        # Routes for Experiences
        # ----------------------------
        from flask import render_template
        from models import Experience, Tour

        # List all experiences (filtered for Manali & Uttarakhand if desired)
        @app.route("/experiences")
        def experiences():
            experiences_list = Experience.query.all()
            return render_template("experiences.html", experiences=experiences_list)

        # Single experience detail page
        @app.route("/experience/<int:exp_id>")
        def experience_detail(exp_id):
            e = Experience.query.get_or_404(exp_id)
            return render_template("experience_detail.html", e=e)

        # Optional: experiences filtered by tour
        @app.route("/tour/<int:tour_id>/experiences")
        def experiences_by_tour(tour_id):
            tour = Tour.query.get_or_404(tour_id)
            experiences_list = tour.experiences
            return render_template("experiences.html", experiences=experiences_list)

        # Create database tables if not exist
        db.create_all()

    return app

# Run the app
if __name__ == "__main__":
    create_app().run(debug=True)
