from flask import request, g
from utils.auth import decode_token
from functools import wraps

def auth_middleware():
    """
    Middleware to check for JWT token in request headers.
    If token is valid, add user_id to flask.g context.
    """
    # Skip token check for non-API routes and authentication endpoints
    path = request.path
    if not path.startswith('/api') or path.startswith('/api/auth/login') or path.startswith('/api/users/register'):
        return
        
    # Check for token in authorization header
    auth_header = request.headers.get('Authorization')
    
    if auth_header:
        parts = auth_header.split()
        if len(parts) == 2 and parts[0].lower() == 'bearer':
            token = parts[1]
            user_id = decode_token(token)
            
            if user_id:
                # Store user_id in flask.g context
                g.user_id = user_id
                return
    
    # If code reaches here, token is either missing or invalid
    g.user_id = None 