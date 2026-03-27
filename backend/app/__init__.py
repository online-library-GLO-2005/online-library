from flask import Flask
from app.utils.errors import AppError
from app.config import Config

from app.extensions import ma, jwt
from app.routes.health import bp as health_bp
from app.routes.books import bp as books_bp


def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp)
    app.register_blueprint(books_bp)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    ma.init_app(app)
    jwt.init_app(app)

    register_blueprints(app)

    # Global error handler
    @app.errorhandler(AppError)
    def handle_app_error(e):
        return {"error": e.__class__.__name__, "message": e.message}, e.status_code

    return app