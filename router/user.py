from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models.user import User
from utils.database import db
from utils.auth import hash_password, verify_password, generate_token, token_required

user_router = Blueprint('user', __name__, url_prefix='/api/users')

@user_router.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    
    # Validate required fields
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if user already exists
    existing_user = User.query.filter(
        (User.username == data['username']) | 
        (User.email == data['email'])
    ).first()
    
    if existing_user:
        return jsonify({'error': 'Username or email already exists'}), 409
    
    # Create new user
    try:
        new_user = User(
            username=data['username'],
            email=data['email'],
            password_hash=hash_password(data['password']),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Generate token
        token = generate_token(new_user.id)
        
        return jsonify({
            'message': 'User registered successfully',
            'user': new_user.to_dict(),
            'token': token
        }), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@user_router.route('/login', methods=['POST'])
def login():
    """Login an existing user"""
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

@user_router.route('/profile', methods=['GET'])
@token_required
def get_profile(user_id):
    """Get current user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@user_router.route('/profile', methods=['PUT'])
@token_required
def update_profile(user_id):
    """Update current user profile"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    
    # Update user fields
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'email' in data:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'error': 'Email already in use'}), 409
        user.email = data['email']
    
    if 'username' in data:
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({'error': 'Username already in use'}), 409
        user.username = data['username']
    
    # Update password if provided
    if 'password' in data:
        user.password_hash = hash_password(data['password'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Profile updated successfully',
            'user': user.to_dict()
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 