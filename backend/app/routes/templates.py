from flask import Blueprint, request
from app.core.templates.template_service import TemplateService
from app.core.templates.validators import TemplateValidator
from app.utils.decorators import auth_required, plan_limit
from app.utils.responses import success_response, error_response, created_response, no_content_response

bp = Blueprint('templates', __name__, url_prefix='/api/templates')

@bp.route('', methods=['GET'])
@auth_required
def get_templates(current_user):
    """
    Get all templates (system + user's)
    
    Query params:
        - format: Filter by format (square, story, a4)
    
    Response:
        {
            "success": true,
            "data": {
                "templates": [...]
            }
        }
    """
    try:
        format_filter = request.args.get('format')
        
        if format_filter:
            templates = TemplateService.get_templates_by_format(current_user, format_filter)
        else:
            templates = TemplateService.get_all_templates(current_user)
        
        return success_response({
            'templates': [t.to_dict() for t in templates]
        })
        
    except Exception as e:
        return error_response('Failed to fetch templates', 500)

@bp.route('/<int:template_id>', methods=['GET'])
@auth_required
def get_template(current_user, template_id):
    """
    Get a single template
    
    Response:
        {
            "success": true,
            "data": {...}
        }
    """
    try:
        template = TemplateService.get_template(template_id, current_user)
        return success_response(template.to_dict())
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Failed to fetch template', 500)

@bp.route('', methods=['POST'])
@auth_required
@plan_limit('template')
def create_template(current_user):
    """
    Create a custom template
    
    Request body:
        {
            "name": "My Template",
            "format": "square",
            "json_definition": {...},
            "background_url": "...",  // optional
            "preview_url": "..."      // optional
        }
    
    Response:
        {
            "success": true,
            "message": "Template created successfully",
            "data": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        # Validate
        is_valid, errors = TemplateValidator.validate_create(data)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Create template
        template = TemplateService.create_template(current_user, data)
        
        return created_response(template.to_dict(), 'Template created successfully')
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Failed to create template', 500)

@bp.route('/<int:template_id>', methods=['PUT'])
@auth_required
def update_template(current_user, template_id):
    """
    Update a template
    
    Request body:
        {
            "name": "Updated Name",  // optional
            "format": "story",       // optional
            ... etc
        }
    
    Response:
        {
            "success": true,
            "message": "Template updated successfully",
            "data": {...}
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        # Update template
        template = TemplateService.update_template(template_id, current_user, data)
        
        return success_response(template.to_dict(), 'Template updated successfully')
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Failed to update template', 500)

@bp.route('/<int:template_id>', methods=['DELETE'])
@auth_required
def delete_template(current_user, template_id):
    """
    Delete a template
    
    Response:
        204 No Content
    """
    try:
        TemplateService.delete_template(template_id, current_user)
        return no_content_response()
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Failed to delete template', 500)

@bp.route('/<int:template_id>/duplicate', methods=['POST'])
@auth_required
@plan_limit('template')
def duplicate_template(current_user, template_id):
    """
    Duplicate a template
    
    Response:
        {
            "success": true,
            "message": "Template duplicated successfully",
            "data": {...}
        }
    """
    try:
        template = TemplateService.duplicate_template(template_id, current_user)
        return created_response(template.to_dict(), 'Template duplicated successfully')
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Failed to duplicate template', 500)
