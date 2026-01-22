from app.extensions import db
from app.models import Product, User
from typing import List, Optional, Dict, Any
from sqlalchemy import or_

class ProductService:
    """Handles product business logic"""
    
    @staticmethod
    def create_product(user: User, data: Dict[str, Any]) -> Product:
        """
        Create a new product
        
        Args:
            user: User creating the product
            data: Product data (name, price, category, etc.)
            
        Returns:
            Product: Created product
            
        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        if not data.get('name'):
            raise ValueError('Product name is required')
        
        if not data.get('price'):
            raise ValueError('Product price is required')
        
        try:
            price = float(data['price'])
            if price < 0:
                raise ValueError('Price must be positive')
        except (ValueError, TypeError):
            raise ValueError('Invalid price format')
        
        # Check for duplicate SKU if provided
        sku = data.get('sku')
        if sku:
            existing = Product.query.filter_by(sku=sku).first()
            if existing:
                raise ValueError(f'Product with SKU {sku} already exists')
        
        # Create product
        product = Product(
            user_id=user.id,
            name=data['name'].strip(),
            price=price,
            category=data.get('category', '').strip() if data.get('category') else None,
            sku=sku.strip() if sku else None,
            description=data.get('description', '').strip() if data.get('description') else None,
            image_url=data.get('image_url')
        )
        
        db.session.add(product)
        db.session.commit()
        
        return product
    
    @staticmethod
    def get_user_products(
        user: User,
        category: Optional[str] = None,
        search: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Get user's products with optional filtering and pagination
        
        Args:
            user: User whose products to fetch
            category: Optional category filter
            search: Optional search query
            page: Page number (1-indexed)
            per_page: Items per page
            
        Returns:
            dict: Paginated products with metadata
        """
        query = Product.query.filter_by(user_id=user.id)
        
        # Apply filters
        if category:
            query = query.filter_by(category=category)
        
        if search:
            search_term = f'%{search}%'
            query = query.filter(
                or_(
                    Product.name.ilike(search_term),
                    Product.sku.ilike(search_term),
                    Product.description.ilike(search_term)
                )
            )
        
        # Order by most recent
        query = query.order_by(Product.created_at.desc())
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'products': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    
    @staticmethod
    def get_product(product_id: int, user: User) -> Product:
        """
        Get a single product by ID
        
        Args:
            product_id: Product ID
            user: User requesting the product
            
        Returns:
            Product: The product
            
        Raises:
            ValueError: If product not found or unauthorized
        """
        product = Product.query.get(product_id)
        
        if not product:
            raise ValueError('Product not found')
        
        if product.user_id != user.id:
            raise ValueError('Unauthorized access to product')
        
        return product
    
    @staticmethod
    def update_product(product_id: int, user: User, data: Dict[str, Any]) -> Product:
        """
        Update a product
        
        Args:
            product_id: Product ID
            user: User updating the product
            data: Updated product data
            
        Returns:
            Product: Updated product
            
        Raises:
            ValueError: If validation fails or unauthorized
        """
        product = ProductService.get_product(product_id, user)
        
        # Update fields
        if 'name' in data and data['name']:
            product.name = data['name'].strip()
        
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    raise ValueError('Price must be positive')
                product.price = price
            except (ValueError, TypeError):
                raise ValueError('Invalid price format')
        
        if 'category' in data:
            product.category = data['category'].strip() if data['category'] else None
        
        if 'sku' in data:
            new_sku = data['sku'].strip() if data['sku'] else None
            if new_sku and new_sku != product.sku:
                # Check for duplicate
                existing = Product.query.filter_by(sku=new_sku).first()
                if existing:
                    raise ValueError(f'Product with SKU {new_sku} already exists')
                product.sku = new_sku
        
        if 'description' in data:
            product.description = data['description'].strip() if data['description'] else None
        
        if 'image_url' in data:
            product.image_url = data['image_url']
        
        db.session.commit()
        
        return product
    
    @staticmethod
    def delete_product(product_id: int, user: User) -> None:
        """
        Delete a product
        
        Args:
            product_id: Product ID
            user: User deleting the product
            
        Raises:
            ValueError: If product not found or unauthorized
        """
        product = ProductService.get_product(product_id, user)
        
        db.session.delete(product)
        db.session.commit()
    
    @staticmethod
    def get_categories(user: User) -> List[str]:
        """
        Get unique categories for user's products
        
        Args:
            user: User whose categories to fetch
            
        Returns:
            List[str]: List of unique categories
        """
        categories = db.session.query(Product.category).filter(
            Product.user_id == user.id,
            Product.category.isnot(None)
        ).distinct().all()
        
        return [c[0] for c in categories if c[0]]
    
    @staticmethod
    def update_product_image(product_id: int, user: User, image_url: str) -> Product:
        """
        Update product image URL
        
        Args:
            product_id: Product ID
            user: User updating the image
            image_url: New image URL
            
        Returns:
            Product: Updated product
        """
        product = ProductService.get_product(product_id, user)
        product.image_url = image_url
        db.session.commit()
        
        return product
