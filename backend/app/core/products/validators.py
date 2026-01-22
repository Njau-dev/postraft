from typing import Dict, Any, List, Tuple

class ProductValidator:
    """Validates product data"""
    
    @staticmethod
    def validate_create(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate product creation data
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        
        # Name validation
        if not data.get('name'):
            errors.append('Product name is required')
        elif len(data['name'].strip()) < 2:
            errors.append('Product name must be at least 2 characters')
        elif len(data['name'].strip()) > 200:
            errors.append('Product name must be less than 200 characters')
        
        # Price validation
        if not data.get('price'):
            errors.append('Product price is required')
        else:
            try:
                price = float(data['price'])
                if price < 0:
                    errors.append('Price must be a positive number')
                if price > 1000000000:
                    errors.append('Price is too large')
            except (ValueError, TypeError):
                errors.append('Price must be a valid number')
        
        # Category validation (optional)
        if data.get('category') and len(data['category']) > 100:
            errors.append('Category must be less than 100 characters')
        
        # SKU validation (optional)
        if data.get('sku') and len(data['sku']) > 100:
            errors.append('SKU must be less than 100 characters')
        
        # Description validation (optional)
        if data.get('description') and len(data['description']) > 5000:
            errors.append('Description must be less than 5000 characters')
        
        return len(errors) == 0, errors
    
    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """
        Validate product update data
        
        Returns:
            tuple: (is_valid, list_of_errors)
        """
        errors = []
        
        # Name validation (if provided)
        if 'name' in data:
            if not data['name']:
                errors.append('Product name cannot be empty')
            elif len(data['name'].strip()) < 2:
                errors.append('Product name must be at least 2 characters')
            elif len(data['name'].strip()) > 200:
                errors.append('Product name must be less than 200 characters')
        
        # Price validation (if provided)
        if 'price' in data:
            try:
                price = float(data['price'])
                if price < 0:
                    errors.append('Price must be a positive number')
                if price > 1000000000:
                    errors.append('Price is too large')
            except (ValueError, TypeError):
                errors.append('Price must be a valid number')
        
        # Category validation (if provided)
        if 'category' in data and data['category'] and len(data['category']) > 100:
            errors.append('Category must be less than 100 characters')
        
        # SKU validation (if provided)
        if 'sku' in data and data['sku'] and len(data['sku']) > 100:
            errors.append('SKU must be less than 100 characters')
        
        # Description validation (if provided)
        if 'description' in data and data['description'] and len(data['description']) > 5000:
            errors.append('Description must be less than 5000 characters')
        
        return len(errors) == 0, errors
