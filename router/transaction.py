from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models.transaction import Transaction, TransactionItem
from models.product import Product
from models.user import User
from utils.database import db
from utils.auth import token_required

transaction_router = Blueprint('transaction', __name__, url_prefix='/api/transactions')

@transaction_router.route('', methods=['GET'])
@token_required
def get_user_transactions(user_id):
    """Get all transactions for a user"""
    try:
        # Query all transactions for the user
        transactions = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.created_at.desc()).all()
        
        # Format response
        transactions_data = [transaction.to_dict() for transaction in transactions]
        
        return jsonify({
            'transactions': transactions_data
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_router.route('/<transaction_id>', methods=['GET'])
@token_required
def get_transaction(user_id, transaction_id):
    """Get a single transaction by ID"""
    try:
        # Query the transaction
        transaction = Transaction.query.get(transaction_id)
        
        if not transaction:
            return jsonify({'error': 'Transaction not found'}), 404
        
        # Check if user is authorized to view this transaction
        if str(transaction.user_id) != str(user_id):
            return jsonify({'error': 'Unauthorized'}), 403
        
        return jsonify(transaction.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@transaction_router.route('', methods=['POST'])
@token_required
def create_transaction(user_id):
    """Create a new transaction"""
    data = request.json
    
    # Validate required fields
    required_fields = ['items']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Validate items format
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return jsonify({'error': 'Items must be a non-empty array'}), 400
    
    # Check if user exists
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Verify all products exist and have sufficient stock
    total_amount = 0
    transaction_items = []
    
    for item_data in data['items']:
        if 'product_id' not in item_data or 'quantity' not in item_data:
            return jsonify({'error': 'Each item must have product_id and quantity'}), 400
        
        try:
            quantity = int(item_data['quantity'])
            if quantity <= 0:
                return jsonify({'error': 'Quantity must be greater than 0'}), 400
        except ValueError:
            return jsonify({'error': 'Invalid quantity format'}), 400
        
        # Get product
        product = Product.query.get(item_data['product_id'])
        if not product:
            return jsonify({'error': f'Product {item_data["product_id"]} not found'}), 404
        
        if not product.is_active:
            return jsonify({'error': f'Product {product.name} is not available'}), 400
        
        if product.stock_quantity < quantity:
            return jsonify({'error': f'Insufficient stock for product {product.name}'}), 400
        
        # Calculate item subtotal
        item_price = product.price
        item_subtotal = item_price * quantity
        total_amount += item_subtotal
        
        # Create transaction item (but don't add to session yet)
        transaction_items.append({
            'product': product,
            'quantity': quantity,
            'price': item_price
        })
    
    try:
        # Create the transaction
        transaction = Transaction(
            user_id=user_id,
            total_amount=total_amount,
            status='pending',
            payment_method=data.get('payment_method'),
            shipping_address=data.get('shipping_address')
        )
        
        db.session.add(transaction)
        db.session.flush()  # This assigns an ID to the transaction
        
        # Create transaction items
        for item in transaction_items:
            transaction_item = TransactionItem(
                transaction_id=transaction.id,
                product_id=item['product'].id,
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(transaction_item)
            
            # Update product stock
            item['product'].stock_quantity -= item['quantity']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction created successfully',
            'transaction': transaction.to_dict()
        }), 201
    
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@transaction_router.route('/<transaction_id>/status', methods=['PUT'])
@token_required
def update_transaction_status(user_id, transaction_id):
    """Update transaction status (admin only for some statuses)"""
    # TODO: Add admin check for certain status changes
    
    data = request.json
    
    if 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    # Allowed statuses
    allowed_statuses = ['pending', 'completed', 'cancelled']
    if data['status'] not in allowed_statuses:
        return jsonify({'error': f'Status must be one of: {", ".join(allowed_statuses)}'}), 400
    
    # Get transaction
    transaction = Transaction.query.get(transaction_id)
    if not transaction:
        return jsonify({'error': 'Transaction not found'}), 404
    
    # Check if user is authorized
    if str(transaction.user_id) != str(user_id):
        # TODO: Check if admin instead of returning error
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        # Update transaction status
        old_status = transaction.status
        transaction.status = data['status']
        
        # If cancelling a transaction, restore product stock
        if data['status'] == 'cancelled' and old_status != 'cancelled':
            for item in transaction.items:
                product = Product.query.get(item.product_id)
                if product:
                    product.stock_quantity += item.quantity
        
        db.session.commit()
        
        return jsonify({
            'message': 'Transaction status updated successfully',
            'transaction': transaction.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 