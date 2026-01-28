from app.extensions import db
from app.models import Template, User
from typing import List, Optional, Dict, Any

class TemplateService:
    """Handles template business logic"""
    
    @staticmethod
    def get_all_templates(user: User) -> List[Template]:
        """
        Get all templates (system + user's custom templates)
        
        Args:
            user: Current user
            
        Returns:
            List[Template]: All accessible templates
        """
        # Get system templates + user's templates
        templates = Template.query.filter(
            db.or_(
                Template.is_system == True,
                Template.user_id == user.id
            )
        ).filter_by(is_active=True).order_by(
            Template.is_system.desc(),
            Template.created_at.desc()
        ).all()
        
        return templates
    
    @staticmethod
    def get_template(template_id: int, user: User) -> Template:
        """
        Get a single template
        
        Args:
            template_id: Template ID
            user: Current user
            
        Returns:
            Template: The template
            
        Raises:
            ValueError: If template not found or unauthorized
        """
        template = Template.query.get(template_id)
        
        if not template:
            raise ValueError('Template not found')
        
        # Check access: system templates or user's own templates
        if not template.is_system and template.user_id != user.id:
            raise ValueError('Unauthorized access to template')
        
        return template
    
    @staticmethod
    def create_template(user: User, data: Dict[str, Any]) -> Template:
        """
        Create a custom template
        
        Args:
            user: User creating the template
            data: Template data
            
        Returns:
            Template: Created template
            
        Raises:
            ValueError: If validation fails
        """
        # Validate required fields
        if not data.get('name'):
            raise ValueError('Template name is required')
        
        if not data.get('format'):
            raise ValueError('Template format is required')
        
        if data['format'] not in ['square', 'story', 'a4']:
            raise ValueError('Invalid format. Must be: square, story, or a4')
        
        if not data.get('json_definition'):
            raise ValueError('Template definition is required')
        
        # Validate JSON structure
        json_def = data['json_definition']
        if not isinstance(json_def, dict):
            raise ValueError('Template definition must be a valid JSON object')
        
        if 'canvas' not in json_def or 'layers' not in json_def:
            raise ValueError('Template must have canvas and layers')
        
        # Create template
        template = Template(
            user_id=user.id,
            name=data['name'].strip(),
            format=data['format'],
            background_url=data.get('background_url'),
            json_definition=json_def,
            preview_url=data.get('preview_url'),
            is_system=False,
            is_active=True
        )
        
        db.session.add(template)
        db.session.commit()
        
        return template
    
    @staticmethod
    def update_template(template_id: int, user: User, data: Dict[str, Any]) -> Template:
        """
        Update a template
        
        Args:
            template_id: Template ID
            user: User updating the template
            data: Updated template data
            
        Returns:
            Template: Updated template
            
        Raises:
            ValueError: If validation fails or unauthorized
        """
        template = TemplateService.get_template(template_id, user)
        
        # Can't edit system templates
        if template.is_system:
            raise ValueError('Cannot edit system templates')
        
        # Update fields
        if 'name' in data and data['name']:
            template.name = data['name'].strip()
        
        if 'format' in data:
            if data['format'] not in ['square', 'story', 'a4']:
                raise ValueError('Invalid format')
            template.format = data['format']
        
        if 'background_url' in data:
            template.background_url = data['background_url']
        
        if 'json_definition' in data:
            json_def = data['json_definition']
            if not isinstance(json_def, dict):
                raise ValueError('Template definition must be a valid JSON object')
            template.json_definition = json_def
        
        if 'preview_url' in data:
            template.preview_url = data['preview_url']
        
        db.session.commit()
        
        return template
    
    @staticmethod
    def delete_template(template_id: int, user: User) -> None:
        """
        Delete a template
        
        Args:
            template_id: Template ID
            user: User deleting the template
            
        Raises:
            ValueError: If template not found or unauthorized
        """
        template = TemplateService.get_template(template_id, user)
        
        # Can't delete system templates
        if template.is_system:
            raise ValueError('Cannot delete system templates')
        
        db.session.delete(template)
        db.session.commit()
    
    @staticmethod
    def get_templates_by_format(user: User, format: str) -> List[Template]:
        """
        Get templates filtered by format
        
        Args:
            user: Current user
            format: Template format (square, story, a4)
            
        Returns:
            List[Template]: Filtered templates
        """
        templates = Template.query.filter(
            db.or_(
                Template.is_system == True,
                Template.user_id == user.id
            )
        ).filter_by(
            format=format,
            is_active=True
        ).order_by(
            Template.is_system.desc(),
            Template.created_at.desc()
        ).all()
        
        return templates
    
    @staticmethod
    def duplicate_template(template_id: int, user: User) -> Template:
        """
        Duplicate a template (useful for customizing system templates)
        
        Args:
            template_id: Template to duplicate
            user: Current user
            
        Returns:
            Template: Duplicated template
        """
        original = TemplateService.get_template(template_id, user)
        
        # Create duplicate
        duplicate = Template(
            user_id=user.id,
            name=f"{original.name} (Copy)",
            format=original.format,
            background_url=original.background_url,
            json_definition=original.json_definition.copy(),
            preview_url=original.preview_url,
            is_system=False,
            is_active=True
        )
        
        db.session.add(duplicate)
        db.session.commit()
        
        return duplicate
