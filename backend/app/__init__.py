from flask import Flask
from app.config import config
from app.extensions import init_extensions
import logging
from logging.handlers import RotatingFileHandler
import os


def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    # Initialize extensions
    init_extensions(app)

    # Configure logging
    configure_logging(app)

    # Configure error handlers
    error_handler(app)

    # Import models to register them with SQLAlchemy
    from app.models import user, plan, product, template, campaign, poster  # noqa: F401 means unused import

    # Register blueprints
    from app.routes import auth, products, templates, posters

    app.register_blueprint(auth.bp)
    app.register_blueprint(products.bp)
    app.register_blueprint(templates.bp)
    app.register_blueprint(posters.bp)  # ISSUE FOR TESTING IS HERE
    # app.register_blueprint(campaigns.bp, url_prefix='/api/campaigns')
    # app.register_blueprint(billing.bp, url_prefix='/api/billing')

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app


def configure_logging(app):
    """Configure logging for the Flask app"""
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler(
        'logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    if app.debug:
        file_handler.setLevel(logging.DEBUG)
        app.logger.setLevel(logging.DEBUG)
    else:
        file_handler.setLevel(logging.INFO)
        app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('PostRaft startup')


def error_handler(app):
    @app.errorhandler(400)
    def bad_request(error):
        return {'error': 'Bad request'}, 400

    @app.errorhandler(401)
    def unauthorized(error):
        return {'error': 'Unauthorized'}, 401

    @app.errorhandler(403)
    def forbidden(error):
        return {'error': 'Forbidden'}, 403

    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {error}')
        return {'error': 'Internal server error'}, 500
