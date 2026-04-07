from flask import Flask
from app.config import Config
from app.middleware.error_handlers import register_error_handlers
from app.middleware.logging import configure_logging

from app.extensions import jwt, cors
from app.routes.health import bp as health_bp
from app.routes.index import bp as index_bp
from app.routes.books_route import bp as books_bp


# Add blueprints of routes in here
def register_blueprints(app: Flask) -> None:
    app.register_blueprint(health_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(books_bp)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    # Middleware config, only filters the /health log
    configure_logging()

    # == Initialize extensions

    # JWT tokens
    jwt.init_app(app)

    # CORS allowed origins
    cors.init_app(app, resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}})

    # == This is where our routes are
    register_blueprints(app)

    # == Register how every error is handled in app
    register_error_handlers(app)

    return app
