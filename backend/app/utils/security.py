from flask_jwt_extended import create_access_token
import bcrypt

# Generate token based on user_id, also putting is_admin(default is false) for protected route.
def generate_token(user_id: str, is_admin: bool = False) -> str:
    return create_access_token(identity=user_id, additional_claims={'is_admin': is_admin})

# Bcrypt for password hashing and comparing
# Bcrypt works with bytes, so we need to encode and decode
def hashPassword(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def comparePassword(password: str, hashedPassword: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashedPassword.encode('utf-8'))