from flask import jsonify

def success_response(data=None, message=None, status=200):
    """
    Standard success response
    
    Args:
        data: Response data
        message: Optional success message
        status: HTTP status code
    """
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status

def error_response(message, status=400, errors=None):
    """
    Standard error response
    
    Args:
        message: Error message
        status: HTTP status code
        errors: Optional detailed errors (validation, etc.)
    """
    response = {
        'success': False,
        'error': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status

def created_response(data, message="Resource created successfully"):
    """Shorthand for 201 Created"""
    return success_response(data, message, 201)

def no_content_response():
    """Shorthand for 204 No Content"""
    return '', 204
