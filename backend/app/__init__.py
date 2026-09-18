import os
from flask import Flask
from dotenv import load_dotenv

from .config import config
from .extensions import db, migrate, jwt, cors, limiter


def create_app(config_name=None):
    """Application factory."""
    load_dotenv()

    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__, static_folder='../uploads', static_url_path='/uploads')
    app.config.from_object(config[config_name])

    # Ensure upload folder exists
    upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), app.config['UPLOAD_FOLDER'])
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER_PATH'] = upload_folder

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config['FRONTEND_URL']}},
        supports_credentials=True
    )
    limiter.init_app(app)

    # Register blueprints
    from .routes.auth import auth_bp
    from .routes.public import public_bp
    from .routes.admin_products import admin_products_bp
    from .routes.admin_categories import admin_categories_bp
    from .routes.admin_dashboard import admin_dashboard_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(public_bp, url_prefix='/api')
    app.register_blueprint(admin_products_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_categories_bp, url_prefix='/api/admin')
    app.register_blueprint(admin_dashboard_bp, url_prefix='/api/admin')

    # Import all models so Flask-Migrate picks them up
    from .models import admin_user, category, product, product_image  # noqa

    # Register CLI commands
    from .seed import register_commands
    register_commands(app)

    @app.errorhandler(404)
    def not_found(e):
        from .utils.responses import error_response
        return error_response('NOT_FOUND', 'Resource not found', 404)

    @app.errorhandler(500)
    def internal_error(e):
        from .utils.responses import error_response
        return error_response('SERVER_ERROR', 'Internal server error', 500)

    @app.errorhandler(413)
    def request_entity_too_large(e):
        from .utils.responses import error_response
        return error_response('FILE_TOO_LARGE', 'File size exceeds the maximum limit of 10MB', 413)

    return app
