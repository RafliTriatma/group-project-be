from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models.product import Product
from utils.database import db
from utils.auth import token_required

product_router = Blueprint('product', __name__, url_prefix='/api/products')

@product_router.route('', methods=['GET'])
def get_products():
    """Get all products with optional filtering"""
    # Get query parameters
    category = request.args.get('category')
    search = request.args.get('search')
    sort_by = request.args.get('sort', 'name')  # Default sort by name
    sort_order = request.args.get('order', 'asc')  # Default ascending order
    limit = request.args.get('limit', 50, type=int)
    page = request.args.get('page', 1, type=int)
    
    # Build query
    query = Product.query.filter_by(is_active=True)
    
    # Apply category filter if provided
    if category:
        query = query.filter_by(category=category)
    
    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Product.name.ilike(search_term)) | 
            (Product.description.ilike(search_term))
        )
    
    # Apply sorting
    if sort_order.lower() == 'desc':
        query = query.order_by(getattr(Product, sort_by).desc())
    else:
        query = query.order_by(getattr(Product, sort_by).asc())
    
    # Apply pagination
    paginated_products = query.paginate(page=page, per_page=limit, error_out=False)
    
    # Format response
    products = [product.to_dict() for product in paginated_products.items]
    
    return jsonify({
        'products': products,
        'total': paginated_products.total,
        'pages': paginated_products.pages,
        'current_page': page
    }), 200

@product_router.route('/<product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if not product.is_active:
        return jsonify({'error': 'Product is not available'}), 410
    
    return jsonify(product.to_dict()), 200

@product_router.route('', methods=['POST'])
@token_required
def create_product(user_id):
    """Create a new product (admin only)"""
    # TODO: Add admin check
    
    data = request.json
    
    # Validate required fields
    required_fields = ['name', 'price']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    try:
        # Create new product
        new_product = Product(
            name=data['name'],
            description=data.get('description'),
            price=float(data['price']),
            stock_quantity=int(data.get('stock_quantity', 0)),
            category=data.get('category'),
            image_url=data.get('image_url')
        )
        
        db.session.add(new_product)
        db.session.commit()
        
        return jsonify({
            'message': 'Product created successfully',
            'product': new_product.to_dict()
        }), 201
    
    except ValueError:
        return jsonify({'error': 'Invalid data format'}), 400
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@product_router.route('/<product_id>', methods=['PUT'])
@token_required
def update_product(user_id, product_id):
    """Update an existing product (admin only)"""
    # TODO: Add admin check
    
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.json
    
    # Update product fields
    if 'name' in data:
        product.name = data['name']
    
    if 'description' in data:
        product.description = data['description']
    
    if 'price' in data:
        try:
            product.price = float(data['price'])
        except ValueError:
            return jsonify({'error': 'Invalid price format'}), 400
    
    if 'stock_quantity' in data:
        try:
            product.stock_quantity = int(data['stock_quantity'])
        except ValueError:
            return jsonify({'error': 'Invalid stock quantity format'}), 400
    
    if 'category' in data:
        product.category = data['category']
    
    if 'image_url' in data:
        product.image_url = data['image_url']
    
    if 'is_active' in data:
        product.is_active = bool(data['is_active'])
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Product updated successfully',
            'product': product.to_dict()
        }), 200
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Database error occurred'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@product_router.route('/<product_id>', methods=['DELETE'])
@token_required
def delete_product(user_id, product_id):
    """Soft delete a product (admin only)"""
    # TODO: Add admin check
    
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Soft delete by setting is_active to False
    product.is_active = False
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Product deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 