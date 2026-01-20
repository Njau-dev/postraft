from app.models import User

class AuthorizationService:
    """Handles user permissions and plan limits"""
    
    @staticmethod
    def can_create_product(user: User) -> tuple[bool, str]:
        """
        Check if user can create more products
        
        Returns:
            tuple: (can_create: bool, error_message: str)
        """
        # Unlimited for Agency plan
        if user.plan.max_products == -1:
            return True, ""
        
        # Check current count
        current_count = user.products.count()
        if current_count >= user.plan.max_products:
            return False, f"Product limit reached ({user.plan.max_products}). Upgrade your plan."
        
        return True, ""
    
    @staticmethod
    def can_create_template(user: User) -> tuple[bool, str]:
        """Check if user can create more templates"""
        if user.plan.max_templates == -1:
            return True, ""
        
        current_count = user.templates.count()
        if current_count >= user.plan.max_templates:
            return False, f"Template limit reached ({user.plan.max_templates}). Upgrade your plan."
        
        return True, ""
    
    @staticmethod
    def can_generate_poster(user: User) -> tuple[bool, str]:
        """Check if user can generate more posters this month"""
        if user.plan.monthly_generations == -1:
            return True, ""
        
        if user.monthly_generations >= user.plan.monthly_generations:
            return False, f"Monthly generation limit reached ({user.plan.monthly_generations}). Upgrade your plan."
        
        return True, ""
    
    @staticmethod
    def has_feature(user: User, feature_name: str) -> bool:
        """
        Check if user's plan has a specific feature
        
        Args:
            user: User object
            feature_name: Feature key (e.g., 'branding_removal', 'batch_export')
            
        Returns:
            bool: True if user has access to feature
        """
        return user.plan.features.get(feature_name, False)
