from flask import Blueprint, request
from app.core.products.product_service import ProductService
from app.core.products.validators import ProductValidator
from app.utils.decorators import auth_required, plan_limit
from app.utils.responses import success_response, error_response, created_response, no_content_response
from app.infrastructure.storage import upload_image, delete_image
from werkzeug.utils import secure_filename
import os

bp = Blueprint('products', __name__, url_prefix='/api/products')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('', methods=['GET'])
@auth_required
def get_products(current_user):
    """
    Get user's products with optional filtering
    
    Query params:
        - category: Filter by category
        - search: Search products
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20)
    
    Response:
        {
            "success": true,
            "data": {
                "products": [...],
                "total": 100,
                "page": 1,
                "per_page": 20,
                "pages": 5,
                "has_next": true,
                "has_prev": false
            }
        }
    """
    try:
        category = request.args.get('category')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Validate pagination
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        result = ProductService.get_user_products(
            current_user,
            category=category,
            search=search,
            page=page,
            per_page=per_page
        )
        
        return success_response(result)
        
    except Exception as e:
        return error_response('Failed to fetch products', 500)

@bp.route('', methods=['POST'])
@auth_required
@plan_limit('product')
def create_product(current_user):
    """
    Create a new product
    
    Request body:
        {
            "name": "Product Name",
            "price": 100.50,
            "category": "Category",  // optional
            "sku": "SKU-123",        // optional
            "description": "..."     // optional
        }
    
    Response:
        {
            "success": true,
            "message": "Product created successfully",
            "data": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        # Validate
        is_valid, errors = ProductValidator.validate_create(data)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Create product
        product = ProductService.create_product(current_user, data)
        
        return created_response(product.to_dict(), 'Product created successfully')
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Failed to create product', 500)

@bp.route('/<int:product_id>', methods=['GET'])
@auth_required
def get_product(current_user, product_id):
    """
    Get a single product
    
    Response:
        {
            "success": true,
            "data": {...}
        }
    """
    try:
        product = ProductService.get_product(product_id, current_user)
        return success_response(product.to_dict())
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Failed to fetch product', 500)

@bp.route('/<int:product_id>', methods=['PUT'])
@auth_required
def update_product(current_user, product_id):
    """
    Update a product
    
    Request body:
        {
            "name": "Updated Name",  // optional
            "price": 150.00,         // optional
            "category": "New Cat",   // optional
            ... etc
        }
    
    Response:
        {
            "success": true,
            "message": "Product updated successfully",
            "data": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        # Validate
        is_valid, errors = ProductValidator.validate_update(data)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Update product
        product = ProductService.update_product(product_id, current_user, data)
        
        return success_response(product.to_dict(), 'Product updated successfully')
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Failed to update product', 500)

@bp.route('/<int:product_id>', methods=['DELETE'])
@auth_required
def delete_product(current_user, product_id):
    """
    Delete a product
    
    Response:
        204 No Content
    """
    try:
        # Get product first to delete image
        product = ProductService.get_product(product_id, current_user)
        
        # Delete image from S3 if exists
        if product.image_url:
            delete_image(product.image_url)
        
        # Delete product
        ProductService.delete_product(product_id, current_user)
        
        return no_content_response()
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Failed to delete product', 500)

@bp.route('/<int:product_id>/image', methods=['POST'])
@auth_required
def upload_product_image(current_user, product_id):
    """
    Upload product image
    
    Request: multipart/form-data with 'image' file
    
    Response:
        {
            "success": true,
            "message": "Image uploaded successfully",
            "data": {
                "image_url": "https://..."
            }
        }
    """
    try:
        # Check if file is present
        if 'image' not in request.files:
            return error_response('No image file provided', 400)
        
        file = request.files['image']
        
        if file.filename == '':
            return error_response('No file selected', 400)
        
        # Validate file
        if not allowed_file(file.filename):
            return error_response(
                f'Invalid file type. Allowed: {", ".join(ALLOWED_EXTENSIONS)}',
                400
            )
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return error_response('File too large. Maximum size: 10MB', 400)
        
        # Get product first (verify ownership)
        product = ProductService.get_product(product_id, current_user)
        
        # Delete old image if exists
        if product.image_url:
            delete_image(product.image_url)

        image_url = upload_image(file, folder='products')
        
        if not image_url:
            return error_response('Failed to upload image', 500)
        
        # Update product
        product = ProductService.update_product_image(product_id, current_user, image_url)
        
        return success_response(
            {'image_url': image_url},
            'Image uploaded successfully'
        )
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Failed to upload image', 500)

@bp.route('/categories', methods=['GET'])
@auth_required
def get_categories(current_user):
    """
    Get unique product categories for current user
    
    Response:
        {
            "success": true,
            "data": {
                "categories": ["groceries", "electronics", ...]
            }
        }
    """
    try:
        categories = ProductService.get_categories(current_user)
        return success_response({'categories': categories})
        
    except Exception as e:
        return error_response('Failed to fetch categories', 500)

@bp.route('/bulk', methods=['POST'])
@auth_required
@plan_limit('product')
def bulk_create_products(current_user):
    """
    Bulk create products (we'll implement CSV upload later)
    
    For now, accepts an array of products
    
    Request body:
        {
            "products": [
                {"name": "...", "price": 100},
                {"name": "...", "price": 200}
            ]
        }
    """
    try:
        data = request.get_json()
        
        if not data or 'products' not in data:
            return error_response('Products array is required', 400)
        
        products_data = data['products']
        
        if not isinstance(products_data, list):
            return error_response('Products must be an array', 400)
        
        if len(products_data) > 100:
            return error_response('Maximum 100 products per bulk upload', 400)
        
        created_products = []
        errors = []
        
        for idx, product_data in enumerate(products_data):
            try:
                # Validate
                is_valid, validation_errors = ProductValidator.validate_create(product_data)
                if not is_valid:
                    errors.append({
                        'index': idx,
                        'errors': validation_errors
                    })
                    continue
                
                # Create product
                product = ProductService.create_product(current_user, product_data)
                created_products.append(product.to_dict())
                
            except Exception as e:
                errors.append({
                    'index': idx,
                    'error': str(e)
                })
        
        return success_response({
            'created': created_products,
            'errors': errors,
            'total_created': len(created_products),
            'total_errors': len(errors)
        }, f'Created {len(created_products)} products')
        
    except Exception as e:
        return error_response('Bulk creation failed', 500)
