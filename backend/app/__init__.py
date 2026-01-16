from flask import Flask
from app.config import config
from app.extensions import init_extensions


def create_app(config_name='default'):
    """Application factory"""
    app = Flask(__name__)

    # Load config
    app.config.from_object(config[config_name])

    # Initialize extensions
    init_extensions(app)

    # Register blueprints
    # from app.routes import auth, products, templates, campaigns, posters, billing
    # app.register_blueprint(auth.bp)
    # app.register_blueprint(products.bp)
    # app.register_blueprint(templates.bp)
    # app.register_blueprint(campaigns.bp)
    # app.register_blueprint(posters.bp)
    # app.register_blueprint(billing.bp)

    @app.route('/health')
    def health():
        return {'status': 'healthy'}, 200

    return app
