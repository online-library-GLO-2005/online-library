from marshmallow import ValidationError
from flask_jwt_extended.exceptions import JWTExtendedException
from app.errors import AppError
from app.utils.apiResponse import error_response
from werkzeug.exceptions import HTTPException


def register_error_handlers(app):

    # JWT(token) error, non authorized.
    @app.errorhandler(JWTExtendedException)
    def handle_jwt_error(e: JWTExtendedException):
        # jwt error doesn't have message
        return error_response(401, str(e))

    # Validation error from Marshmallow schemas
    @app.errorhandler(ValidationError)
    def handle_validation_error(e: ValidationError):
        return error_response(400, e.messages)

    # Custom application error class
    @app.errorhandler(AppError)
    def handle_app_error(e: AppError):
        return error_response(e.status_code, e.message)

    # Handles every HTTPException
    # Also handles internal server error 500 for unhandled app errors or others
    @app.errorhandler(Exception)
    def handle_generic_error(e: Exception):
        if isinstance(e, HTTPException):
            # Every HTTPException
            return error_response(e.code or 500, e.description)
        return error_response(500, "Internal server error")
