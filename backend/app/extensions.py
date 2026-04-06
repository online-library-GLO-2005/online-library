from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Initialize Flask extension
ma = Marshmallow()
jwt = JWTManager()
cors = CORS()