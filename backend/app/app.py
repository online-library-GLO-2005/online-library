from flask import Flask
from extensions import db, ma, jwt
from routes.books import bp as books_bp
from utils.errors import AppError

# Config class
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)

    # Register blueprints
        # put blueprints here

    # Global error handler
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return {"error": e.__class__.__name__, "message": e.message}, e.status_code

    return app


# Only run if executed directly
if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  # creates tables based on models
    app.run(debug=True)