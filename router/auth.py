from flask import Blueprint, request, jsonify
from models.user import User
from utils.auth import verify_password, generate_token, token_required

auth_router = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_router.route('/login', methods=['POST'])
def login():
    """Login endpoint"""
    data = request.json
    
    # Validate required fields
    if not data.get('username') and not data.get('email'):
        return jsonify({'error': 'Either username or email is required'}), 400
    
    if not data.get('password'):
        return jsonify({'error': 'Password is required'}), 400
    
    # Find user by username or email
    if data.get('username'):
        user = User.query.filter_by(username=data['username']).first()
    else:
        user = User.query.filter_by(email=data['email']).first()
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Verify password
    if not verify_password(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid password'}), 401
    
    # Generate token
    token = generate_token(user.id)
    
    return jsonify({
        'message': 'Login successful',
        'user': user.to_dict(),
        'token': token
    }), 200

@auth_router.route('/verify', methods=['GET'])
@token_required
def verify_token(user_id):
    """Verify a JWT token and return user info"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'message': 'Token is valid',
        'user': user.to_dict()
    }), 200 