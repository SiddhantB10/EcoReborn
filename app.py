"""
EcoReborn Flask Application
A sustainable fashion website with server-side rendering (zero JavaScript).
"""

import os
import logging
from datetime import timedelta
from flask import Flask, session
from flask_login import LoginManager, UserMixin
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class UserLogin(UserMixin):
    """User class for Flask-Login."""
    
    def __init__(self, user_id, email, name):
        self.id = user_id
        self.email = email
        self.name = name
    
    def get_id(self):
        return self.id


def create_app():
    """Application factory pattern."""
    app = Flask(__name__)
    
    # Configuration
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['MONGODB_URI'] = os.getenv('MONGODB_URI')
    app.config['MONGODB_DB_NAME'] = os.getenv('MONGODB_DB_NAME', 'ecoreborn')
    
    # Email configuration
    app.config['SMTP_HOST'] = os.getenv('SMTP_HOST')
    app.config['SMTP_PORT'] = int(os.getenv('SMTP_PORT', 587))
    app.config['SMTP_USER'] = os.getenv('SMTP_USER')
    app.config['SMTP_PASS'] = os.getenv('SMTP_PASS')
    app.config['SMTP_FROM'] = os.getenv('SMTP_FROM', 'noreply@ecoreborn.example')
    app.config['ADMIN_EMAIL'] = os.getenv('ADMIN_EMAIL', 'admin@ecoreborn.example')
    
    # Upload configuration
    app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', './uploads')
    app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 2097152))  # 2MB default
    
    # Session configuration
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
    app.config['SESSION_COOKIE_HTTPONLY'] = os.getenv('SESSION_COOKIE_HTTPONLY', 'True').lower() == 'true'
    app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(seconds=int(os.getenv('PERMANENT_SESSION_LIFETIME', 3600)))
    
    # Application URL
    app.config['APP_URL'] = os.getenv('APP_URL', 'http://localhost:5000')
    
    # Logging (Vercel-compatible: only use StreamHandler in production)
    if os.getenv('FLASK_ENV') == 'production':
        # In production (Vercel), only log to console (read-only filesystem)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[logging.StreamHandler()]
        )
    else:
        # In development, log to both file and console
        log_dir = os.path.join(app.root_path, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(os.path.join(log_dir, 'app.log')),
                logging.StreamHandler()
            ]
        )
    
    # Initialize MongoDB
    try:
        mongo_client = MongoClient(
            app.config['MONGODB_URI'],
            serverSelectionTimeoutMS=5000
        )
        # Test connection
        mongo_client.server_info()
        app.db = mongo_client[app.config['MONGODB_DB_NAME']]
        app.logger.info('MongoDB connection established')
    except ServerSelectionTimeoutError as e:
        app.logger.error(f'Failed to connect to MongoDB: {e}')
        raise Exception('Cannot connect to MongoDB. Please check your connection string.')
    
    # Initialize extensions
    csrf = CSRFProtect(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please login to access this page.'
    login_manager.login_message_category = 'info'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Load user for Flask-Login."""
        from models import User
        user = User.find_by_id(app.db, user_id)
        if user:
            return UserLogin(str(user['_id']), user['email'], user['name'])
        return None
    
    # Initialize rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=os.getenv('RATELIMIT_STORAGE_URL', 'memory://')
    )
    
    # Apply rate limiting to auth routes
    from auth import auth_bp
    limiter.limit("10 per hour")(auth_bp)
    
    # Register blueprints
    from routes import main_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    
    # Jinja2 filters
    @app.template_filter('datetime')
    def format_datetime_filter(value, format='%B %d, %Y'):
        """Format datetime in templates."""
        if value is None:
            return ''
        from datetime import datetime
        if isinstance(value, datetime):
            return value.strftime(format)
        return value
    
    # Context processors
    @app.context_processor
    def inject_year():
        """Inject current year into all templates."""
        from datetime import datetime
        return {'current_year': datetime.now().year}
    
    @app.context_processor
    def inject_forms():
        """Inject newsletter form into all templates."""
        from forms import NewsletterForm
        return {'footer_newsletter_form': NewsletterForm()}
    
    return app


# Create app instance
app = create_app()


if __name__ == '__main__':
    # Run the application
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV') == 'development'
    
    app.logger.info(f'Starting EcoReborn application on port {port}')
    app.run(host='0.0.0.0', port=port, debug=debug)
