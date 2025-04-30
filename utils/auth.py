import bcrypt
import uuid
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import request, jsonify, current_app

def hash_password(password):
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(stored_password, provided_password):
    """Verify a stored password against the provided password."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password.encode('utf-8'))

def generate_token(user_id, expiration_hours=24):
    """Generate a JWT token."""
    payload = {
        'exp': datetime.utcnow() + timedelta(hours=expiration_hours),
        'iat': datetime.utcnow(),
        'sub': str(user_id)
    }
    return jwt.encode(
        payload,
        current_app.config.get('SECRET_KEY', 'dev-key'),
        algorithm='HS256'
    )

def decode_token(token):
    """Decode a JWT token."""
    try:
        payload = jwt.decode(
            token,
            current_app.config.get('SECRET_KEY', 'dev-key'),
            algorithms=['HS256']
        )
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def token_required(f):
    """Decorator to require a valid token for a route."""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            parts = auth_header.split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        user_id = decode_token(token)
        if not user_id:
            return jsonify({'message': 'Token is invalid or expired'}), 401
        
        # Add user_id to kwargs
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)
    
    return decorated 