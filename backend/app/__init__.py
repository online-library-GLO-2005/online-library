from flask import Flask
from app.extensions import ma, jwt
from app.routes.books import bp as books_bp
from app.utils.errors import AppError

# Config class
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    ma.init_app(app)
    jwt.init_app(app)

    # Register blueprints
    app.register_blueprint(books_bp)

    # Global error handler
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return {"error": e.__class__.__name__, "message": e.message}, e.status_code

    return app


# Only run if executed directly
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)