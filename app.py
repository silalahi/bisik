import logging
from web.app_factory import create_app
from config.settings import AppConfig

# Setup logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    # Load configuration
    config = AppConfig()
    
    # Create Flask app
    app = create_app(config)
    
    # Run server
    app.run(
        debug=config.debug,
        host=config.host,
        port=config.port
    )