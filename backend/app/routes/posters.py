from flask import Blueprint, request, send_file
from app.core.posters.generation_service import PosterGenerationService
from app.utils.decorators import auth_required, plan_limit
from app.utils.responses import success_response, error_response, created_response, no_content_response
from io import BytesIO
import zipfile
import requests

bp = Blueprint('posters', __name__, url_prefix='/api/posters')

@bp.route('/generate', methods=['POST'])
@auth_required
@plan_limit('generation')
def generate_posters(current_user):
    """
    Queue poster generation
    
    Request body:
        {
            "template_id": 1,
            "product_ids": [1, 2, 3],
            "campaign_id": 1  // optional
        }
    
    Response:
        {
            "success": true,
            "message": "Posters queued for generation",
            "data": {
                "job_id": "...",
                "type": "batch",
                "total": 3
            }
        }
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('Request body is required', 400)
        
        template_id = data.get('template_id')
        product_ids = data.get('product_ids', [])
        campaign_id = data.get('campaign_id')
        
        if not template_id:
            return error_response('template_id is required', 400)
        
        if not product_ids or not isinstance(product_ids, list):
            return error_response('product_ids must be a non-empty array', 400)
        
        # Queue generation
        result = PosterGenerationService.queue_generation(
            user=current_user,
            template_id=template_id,
            product_ids=product_ids,
            campaign_id=campaign_id
        )
        
        return created_response(
            result,
            f'{"Poster" if result["total"] == 1 else "Posters"} queued for generation'
        )
        
    except ValueError as e:
        return error_response(str(e), 400)
    except Exception as e:
        return error_response('Failed to queue poster generation', 500)

@bp.route('/job/<job_id>', methods=['GET'])
@auth_required
def get_job_status(current_user, job_id):
    """
    Get job status
    
    Response:
        {
            "success": true,
            "data": {
                "status": "completed",
                "created_at": "...",
                "result": {...}
            }
        }
    """
    try:
        status = PosterGenerationService.get_job_status(job_id)
        return success_response(status)
        
    except Exception as e:
        return error_response('Failed to fetch job status', 500)

@bp.route('', methods=['GET'])
@auth_required
def get_posters(current_user):
    """
    Get user's posters
    
    Query params:
        - product_id: Filter by product
        - template_id: Filter by template
        - campaign_id: Filter by campaign
        - status: Filter by status (generated, failed)
        - page: Page number
        - per_page: Items per page
    
    Response:
        {
            "success": true,
            "data": {
                "posters": [...],
                "total": 100,
                "page": 1,
                "pages": 5
            }
        }
    """
    try:
        product_id = request.args.get('product_id', type=int)
        template_id = request.args.get('template_id', type=int)
        campaign_id = request.args.get('campaign_id', type=int)
        status = request.args.get('status')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Validate pagination
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        result = PosterGenerationService.get_user_posters(
            user=current_user,
            product_id=product_id,
            template_id=template_id,
            campaign_id=campaign_id,
            status=status,
            page=page,
            per_page=per_page
        )
        
        return success_response(result)
        
    except Exception as e:
        return error_response('Failed to fetch posters', 500)

@bp.route('/<int:poster_id>', methods=['GET'])
@auth_required
def get_poster(current_user, poster_id):
    """
    Get a single poster
    
    Response:
        {
            "success": true,
            "data": {...}
        }
    """
    try:
        poster = PosterGenerationService.get_poster(poster_id, current_user)
        return success_response(poster.to_dict())
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Failed to fetch poster', 500)

@bp.route('/<int:poster_id>', methods=['DELETE'])
@auth_required
def delete_poster(current_user, poster_id):
    """
    Delete a poster
    
    Response:
        204 No Content
    """
    try:
        PosterGenerationService.delete_poster(poster_id, current_user)
        return no_content_response()
        
    except ValueError as e:
        return error_response(str(e), 404)
    except Exception as e:
        return error_response('Failed to delete poster', 500)

@bp.route('/download', methods=['POST'])
@auth_required
def download_posters(current_user):
    """
    Download multiple posters as ZIP
    
    Request body:
        {
            "poster_ids": [1, 2, 3]
        }
    
    Response:
        ZIP file download
    """
    try:
        data = request.get_json()
        poster_ids = data.get('poster_ids', [])
        
        if not poster_ids or not isinstance(poster_ids, list):
            return error_response('poster_ids must be a non-empty array', 400)
        
        # Create ZIP file in memory
        zip_buffer = BytesIO()
        
        with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
            for poster_id in poster_ids:
                try:
                    poster = PosterGenerationService.get_poster(poster_id, current_user)
                    
                    if poster.status != 'generated' or not poster.image_url:
                        continue
                    
                    # Download image
                    response = requests.get(poster.image_url, timeout=30)
                    response.raise_for_status()
                    
                    # Add to ZIP
                    filename = f"poster_{poster.id}_{poster.product.name[:30]}.png"
                    # Sanitize filename
                    filename = "".join(c for c in filename if c.isalnum() or c in (' ', '_', '-', '.')).strip()
                    
                    zip_file.writestr(filename, response.content)
                    
                except Exception as e:
                    print(f"Error adding poster {poster_id} to ZIP: {e}")
                    continue
        
        zip_buffer.seek(0)
        
        return send_file(
            zip_buffer,
            mimetype='application/zip',
            as_attachment=True,
            download_name='posters.zip'
        )
        
    except Exception as e:
        return error_response('Failed to create download', 500)

@bp.route('/stats', methods=['GET'])
@auth_required
def get_stats(current_user):
    """
    Get generation statistics
    
    Response:
        {
            "success": true,
            "data": {
                "used": 10,
                "limit": 50,
                "remaining": 40,
                "total_posters": 25
            }
        }
    """
    try:
        stats = PosterGenerationService.get_generation_stats(current_user)
        return success_response(stats)
        
    except Exception as e:
        return error_response('Failed to fetch statistics', 500)
