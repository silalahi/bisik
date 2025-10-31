from flask import Flask
from config.settings import AppConfig
from web.routes import register_routes
import logging


def create_app(config: AppConfig) -> Flask:
    app = Flask(__name__)
    app.config['UPLOAD_FOLDER'] = str(config.upload_folder)
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Register routes
    register_routes(app, config)

    # Add headers to prevent caching during development
    @app.after_request
    def add_header(response):
        if config.debug:
            response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
            response.headers['Pragma'] = 'no-cache'
            response.headers['Expires'] = '0'
        return response
    
    return app