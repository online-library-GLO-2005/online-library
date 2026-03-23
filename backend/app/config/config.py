class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:password@localhost/library"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "secret-key"
    DEBUG = True