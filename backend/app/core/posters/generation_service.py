from app.extensions import db
from app.models import Poster, Product, Template, Campaign, User
from app.workers.batch_job import enqueue_single_poster, enqueue_batch_posters
from app.workers.queue_manager import QueueManager
from typing import List, Dict, Any, Optional
from sqlalchemy import desc

class PosterGenerationService:
    """Handles poster generation business logic"""
    
    @staticmethod
    def queue_generation(
        user: User,
        template_id: int,
        product_ids: List[int],
        campaign_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Queue poster generation jobs
        
        Args:
            user: Current user
            template_id: Template ID
            product_ids: List of product IDs
            campaign_id: Optional campaign ID
            
        Returns:
            dict: Job information
            
        Raises:
            ValueError: If validation fails
        """
        # Validate template
        template = Template.query.get(template_id)
        if not template:
            raise ValueError('Template not found')
        
        # Check template access
        if not template.is_system and template.user_id != user.id:
            raise ValueError('Unauthorized access to template')
        
        # Validate products
        if not product_ids or len(product_ids) == 0:
            raise ValueError('At least one product is required')
        
        # Check all products belong to user
        products = Product.query.filter(
            Product.id.in_(product_ids),
            Product.user_id == user.id
        ).all()
        
        if len(products) != len(product_ids):
            raise ValueError('Some products not found or unauthorized')
        
        # Validate campaign if provided
        if campaign_id:
            campaign = Campaign.query.get(campaign_id)
            if not campaign or campaign.user_id != user.id:
                raise ValueError('Campaign not found or unauthorized')
        
        # Check generation limits
        remaining = PosterGenerationService._check_generation_limit(user, len(product_ids))
        if remaining < len(product_ids):
            raise ValueError(
                f'Monthly generation limit exceeded. You can generate {remaining} more posters this month.'
            )
        
        # Queue job(s)
        if len(product_ids) == 1:
            # Single poster
            job_id = enqueue_single_poster(
                template_id=template_id,
                product_id=product_ids[0],
                user_id=user.id,
                campaign_id=campaign_id
            )
            
            return {
                'job_id': job_id,
                'type': 'single',
                'template_id': template_id,
                'product_ids': product_ids,
                'total': 1
            }
        else:
            # Batch generation
            job_id = enqueue_batch_posters(
                template_id=template_id,
                product_ids=product_ids,
                user_id=user.id,
                campaign_id=campaign_id
            )
            
            return {
                'job_id': job_id,
                'type': 'batch',
                'template_id': template_id,
                'product_ids': product_ids,
                'total': len(product_ids)
            }
    
    @staticmethod
    def get_job_status(job_id: str) -> Dict[str, Any]:
        """
        Get job status
        
        Args:
            job_id: Job ID
            
        Returns:
            dict: Job status information
        """
        return QueueManager.get_job_status(job_id)
    
    @staticmethod
    def get_user_posters(
        user: User,
        product_id: Optional[int] = None,
        template_id: Optional[int] = None,
        campaign_id: Optional[int] = None,
        status: Optional[str] = None,
        page: int = 1,
        per_page: int = 20
    ) -> Dict[str, Any]:
        """
        Get user's generated posters with filtering and pagination
        
        Args:
            user: Current user
            product_id: Filter by product
            template_id: Filter by template
            campaign_id: Filter by campaign
            status: Filter by status
            page: Page number
            per_page: Items per page
            
        Returns:
            dict: Paginated posters
        """
        query = Poster.query.filter_by(user_id=user.id)
        
        # Apply filters
        if product_id:
            query = query.filter_by(product_id=product_id)
        
        if template_id:
            query = query.filter_by(template_id=template_id)
        
        if campaign_id:
            query = query.filter_by(campaign_id=campaign_id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Order by most recent
        query = query.order_by(desc(Poster.created_at))
        
        # Paginate
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return {
            'posters': [p.to_dict() for p in pagination.items],
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'has_next': pagination.has_next,
            'has_prev': pagination.has_prev
        }
    
    @staticmethod
    def get_poster(poster_id: int, user: User) -> Poster:
        """
        Get a single poster
        
        Args:
            poster_id: Poster ID
            user: Current user
            
        Returns:
            Poster: The poster
            
        Raises:
            ValueError: If not found or unauthorized
        """
        poster = Poster.query.get(poster_id)
        
        if not poster:
            raise ValueError('Poster not found')
        
        if poster.user_id != user.id:
            raise ValueError('Unauthorized access to poster')
        
        return poster
    
    @staticmethod
    def delete_poster(poster_id: int, user: User) -> None:
        """
        Delete a poster
        
        Args:
            poster_id: Poster ID
            user: Current user
            
        Raises:
            ValueError: If not found or unauthorized
        """
        poster = PosterGenerationService.get_poster(poster_id, user)
        
        # TODO: Delete image from S3 if needed
        # from app.infrastructure.storage import delete_image
        # if poster.image_url:
        #     delete_image(poster.image_url)
        
        db.session.delete(poster)
        db.session.commit()
    
    @staticmethod
    def _check_generation_limit(user: User, count: int) -> int:
        """
        Check if user can generate more posters
        
        Args:
            user: Current user
            count: Number of posters to generate
            
        Returns:
            int: Remaining generations available
        """
        max_generations = user.plan.monthly_generations
        
        # Unlimited
        if max_generations == -1:
            return float('inf')
        
        current_usage = user.monthly_generations
        remaining = max_generations - current_usage
        
        return max(0, remaining)
    
    @staticmethod
    def get_generation_stats(user: User) -> Dict[str, Any]:
        """
        Get generation statistics for user
        
        Args:
            user: Current user
            
        Returns:
            dict: Generation statistics
        """
        return {
            'used': user.monthly_generations,
            'limit': user.plan.monthly_generations,
            'remaining': PosterGenerationService._check_generation_limit(user, 0),
            'unlimited': user.plan.monthly_generations == -1,
            'total_posters': Poster.query.filter_by(user_id=user.id).count(),
            'successful': Poster.query.filter_by(user_id=user.id, status='generated').count(),
            'failed': Poster.query.filter_by(user_id=user.id, status='failed').count(),
        }
