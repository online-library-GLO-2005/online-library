from flask import jsonify
from typing import Any


# API format of response if success
def success_response(
    status_code: int, data: dict[str, Any] | None = None, message: str = ""
):
    resp: dict[str, Any] = {}
    resp["success"] = True

    if data:
        resp["data"] = data

    if message:
        resp["message"] = message

    return jsonify(resp), status_code


# API format of response if error
def error_response(status_code: int, error: Any):
    if isinstance(error, dict):  # mainly for marshmallow validation
        error_msg = error
    elif isinstance(error, list):  # mainly for marshmallow validation
        error_msg = {"errors": error}
    else:
        error_msg = str(error) if error else "An error occurred"

    resp: dict[str, Any] = {}
    resp["success"] = False
    resp["error"] = error_msg
    return jsonify(resp), status_code
