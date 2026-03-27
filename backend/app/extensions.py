import pymysql.cursors
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager

ma = Marshmallow()
jwt = JWTManager()

def get_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',  # Mettre mot de passe ici
        db='onlineLibrary',   # DB name
        autocommit=True,
        cursorclass=pymysql.cursors.DictCursor
    )