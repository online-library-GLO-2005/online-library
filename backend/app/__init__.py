import os

from flask import Flask, send_from_directory
from app.config import Config
from app.middleware.error_handlers import register_error_handlers
from app.middleware.logging import configure_logging

from app.extensions import jwt, cors


route_modules = [
    "app.routes.health",
    "app.routes.index",
    "app.routes.books_route",
    "app.routes.auth_route",
    "app.routes.authors_route",
    "app.routes.comments_route",
    "app.routes.genres_route",
    "app.routes.publishers_route",
    "app.routes.search_route",
    "app.routes.users_route",
    "app.routes.media_route",
]


# Add blueprints of routes in here
def register_blueprints(app: Flask) -> None:
    for module_path in route_modules:
        module = __import__(module_path, fromlist=["bp"])
        app.register_blueprint(module.bp)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.url_map.strict_slashes = False

    # Middleware config, only filters the /health log
    configure_logging()

    # Route pour servir les PDF
    @app.route('/media/books/<filename>')
    def serve_book(filename):
        # On définit le chemin vers le dossier media
        media_path = os.path.join(app.root_path, '..', 'media', 'books')
        return send_from_directory(media_path, filename)

    # == Initialize extensions

    # JWT tokens
    jwt.init_app(app)

    # CORS allowed origins
    cors.init_app(
        app,
        resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}},
        supports_credentials=True,
    )

    # == This is where our routes are
    register_blueprints(app)

    # == Register how every error is handled in app
    register_error_handlers(app)

    return app
