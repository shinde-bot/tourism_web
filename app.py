from flask import Flask
from config import Config
from extensions import db
from flask_cors import CORS
from flask_mail import Mail

mail = Mail()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    db.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from api.routes import api_bp
        from views.routes import views_bp

        app.register_blueprint(api_bp, url_prefix="/api")
        app.register_blueprint(views_bp)

        db.create_all()
    return app

if __name__ == "__main__":
    create_app().run(debug=True)
