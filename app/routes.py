from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

main_bp = Blueprint('main', __name__)

@main_bp.route("/")
def hello_world():
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running'
    })

@main_bp.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'Service is running'
    })

@main_bp.route('/protected')
@jwt_required()
def protected():
    """Protected endpoint that requires JWT authentication."""
    return jsonify({
        'message': 'This is a protected endpoint'
    }) 