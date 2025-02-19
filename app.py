from flask import Flask
from flask_cors import CORS # type: ignore
from flask_bcrypt import Bcrypt # type: ignore
from flask_jwt_extended import JWTManager # type: ignore
from config import Config
from routes.auth import auth_bp
from routes.staff import staff_bp
from routes.items import items_bp
from routes.categories import categories_bp
from routes.department import department_bp


def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__)
    CORS(app)  # Allow cross-origin requests
    
    # Load configuration from the Config object
    app.config.from_object(Config)
    url = app.config['BASE_URL']

    # Initialize extensions
    bcrypt = Bcrypt(app)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix=f'{url}/auth')
    app.register_blueprint(staff_bp, url_prefix=f'{url}/staff')
    app.register_blueprint(items_bp, url_prefix=f'{url}/items')
    app.register_blueprint(categories_bp, url_prefix=f'{url}/categories')
    app.register_blueprint(department_bp, url_prefix=f'{url}/departments')
    
    return app

# Create the app
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
