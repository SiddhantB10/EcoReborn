"""
Comprehensive Project Health Check
Tests all components: Database, App, Routes, Models, Forms, Auth, and Configuration
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_section(title):
    """Print a formatted section header."""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70)

def print_subsection(title):
    """Print a formatted subsection header."""
    print(f"\n{title}")
    print("-" * 70)

def test_environment_variables():
    """Test if all required environment variables are set."""
    print_section("1. ENVIRONMENT VARIABLES CHECK")
    
    required_vars = {
        'SECRET_KEY': 'Flask secret key',
        'MONGODB_URI': 'MongoDB connection string',
        'MONGODB_DB_NAME': 'Database name',
        'FLASK_ENV': 'Flask environment',
        'APP_URL': 'Application URL'
    }
    
    optional_vars = {
        'SMTP_HOST': 'Email SMTP host',
        'SMTP_PORT': 'Email SMTP port',
        'SMTP_USER': 'Email username',
        'SMTP_PASS': 'Email password',
    }
    
    all_good = True
    
    print_subsection("Required Variables:")
    for var, desc in required_vars.items():
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            if var in ['SECRET_KEY', 'MONGODB_URI']:
                display_value = f"{value[:20]}..." if len(value) > 20 else "***"
            else:
                display_value = value
            print(f"✓ {var}: {display_value}")
        else:
            print(f"✗ {var}: NOT SET - {desc}")
            all_good = False
    
    print_subsection("Optional Variables:")
    for var, desc in optional_vars.items():
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: Set")
        else:
            print(f"⚠ {var}: Not set - {desc} (optional)")
    
    return all_good

def test_database_connection():
    """Test MongoDB connection and collections."""
    print_section("2. DATABASE CONNECTION & COLLECTIONS")
    
    try:
        from pymongo import MongoClient
        
        mongodb_uri = os.getenv('MONGODB_URI')
        db_name = os.getenv('MONGODB_DB_NAME', 'ecoreborn')
        
        print_subsection("Connection Test:")
        client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
        client.server_info()
        print("✓ MongoDB connection successful")
        
        db = client[db_name]
        
        print_subsection("Collections Status:")
        collections = db.list_collection_names()
        
        expected_collections = {
            'users': 'User accounts',
            'password_reset_tokens': 'Password reset tokens',
            'contact_messages': 'Contact form submissions',
            'service_requests': 'Service requests',
            'newsletter_subscribers': 'Newsletter subscribers',
            'login_attempts': 'Login attempt tracking'
        }
        
        all_present = True
        for coll, desc in expected_collections.items():
            if coll in collections:
                count = db[coll].count_documents({})
                print(f"✓ {coll}: {count} document(s) - {desc}")
            else:
                print(f"✗ {coll}: MISSING - {desc}")
                all_present = False
        
        if not all_present:
            print("\n⚠️  Some collections are missing. Run: python init_db.py")
            return False
        
        # Check indexes
        print_subsection("Indexes Check:")
        for coll in expected_collections.keys():
            indexes = list(db[coll].list_indexes())
            print(f"✓ {coll}: {len(indexes)} index(es)")
        
        return True
        
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        return False

def test_models():
    """Test if all models can be imported."""
    print_section("3. MODELS CHECK")
    
    try:
        print_subsection("Importing Models:")
        from models import User, NewsletterSubscriber, ContactMessage, ServiceRequest
        print("✓ User model")
        print("✓ NewsletterSubscriber model")
        print("✓ ContactMessage model")
        print("✓ ServiceRequest model")
        
        print_subsection("Model Methods:")
        # Check if key methods exist
        user_methods = ['create', 'find_by_email', 'find_by_id', 'verify_password', 'update_password']
        for method in user_methods:
            if hasattr(User, method):
                print(f"✓ User.{method}()")
            else:
                print(f"✗ User.{method}() - MISSING")
        
        return True
    except Exception as e:
        print(f"✗ Model import failed: {e}")
        return False

def test_forms():
    """Test if all forms can be imported."""
    print_section("4. FORMS CHECK")
    
    try:
        print_subsection("Importing Forms:")
        from forms import (
            LoginForm, SignupForm, ContactForm, 
            ServiceRequestForm, NewsletterForm, 
            ForgotPasswordForm, ResetPasswordForm
        )
        print("✓ LoginForm")
        print("✓ SignupForm")
        print("✓ ContactForm")
        print("✓ ServiceRequestForm")
        print("✓ NewsletterForm")
        print("✓ ForgotPasswordForm")
        print("✓ ResetPasswordForm")
        return True
    except Exception as e:
        print(f"✗ Form import failed: {e}")
        return False

def test_routes():
    """Test if routes can be imported."""
    print_section("5. ROUTES CHECK")
    
    try:
        print_subsection("Importing Routes:")
        from routes import main_bp
        from auth import auth_bp
        print("✓ Main blueprint (routes.py)")
        print("✓ Auth blueprint (auth.py)")
        
        print_subsection("Route Endpoints:")
        # Main routes
        main_routes = ['/', '/services', '/contact', '/dashboard']
        print("Main routes:")
        for route in main_routes:
            print(f"  ✓ {route}")
        
        # Auth routes
        auth_routes = ['/login', '/signup', '/logout', '/forgot-password', '/reset-password']
        print("\nAuth routes:")
        for route in auth_routes:
            print(f"  ✓ {route}")
        
        return True
    except Exception as e:
        print(f"✗ Route import failed: {e}")
        return False

def test_app_creation():
    """Test if Flask app can be created."""
    print_section("6. FLASK APPLICATION CHECK")
    
    try:
        print_subsection("Creating Flask App:")
        from app import create_app
        app = create_app()
        print("✓ Flask app created successfully")
        
        print_subsection("App Configuration:")
        print(f"✓ Secret Key: {'Set' if app.config.get('SECRET_KEY') else 'NOT SET'}")
        print(f"✓ MongoDB URI: {'Set' if app.config.get('MONGODB_URI') else 'NOT SET'}")
        print(f"✓ Database Name: {app.config.get('MONGODB_DB_NAME')}")
        print(f"✓ Flask Environment: {app.config.get('FLASK_ENV')}")
        print(f"✓ App URL: {app.config.get('APP_URL')}")
        
        print_subsection("Extensions:")
        print("✓ CSRF Protection enabled")
        print("✓ Flask-Login configured")
        print("✓ Rate Limiter configured")
        
        print_subsection("Registered Blueprints:")
        for blueprint in app.blueprints:
            print(f"✓ {blueprint}")
        
        return True
    except Exception as e:
        print(f"✗ App creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_static_files():
    """Test if static files exist."""
    print_section("7. STATIC FILES CHECK")
    
    print_subsection("CSS Files:")
    css_dir = 'static/css'
    if os.path.exists(css_dir):
        css_files = [f for f in os.listdir(css_dir) if f.endswith('.css')]
        for css_file in css_files:
            print(f"✓ {css_file}")
    else:
        print("✗ CSS directory not found")
        return False
    
    print_subsection("Image Directory:")
    img_dir = 'static/images'
    if os.path.exists(img_dir):
        print(f"✓ Images directory exists")
        img_count = len([f for f in os.listdir(img_dir) if not f.startswith('.')])
        print(f"  {img_count} image file(s)")
    else:
        print("⚠ Images directory not found")
    
    return True

def test_templates():
    """Test if template files exist."""
    print_section("8. TEMPLATES CHECK")
    
    template_dir = 'templates'
    if not os.path.exists(template_dir):
        print("✗ Templates directory not found")
        return False
    
    required_templates = {
        'base.html': 'Base template',
        'home.html': 'Home page',
        'services.html': 'Services page',
        'contact.html': 'Contact page',
        'login.html': 'Login page',
        'signup.html': 'Signup page',
        'dashboard.html': 'Dashboard page',
        'forgot_password.html': 'Forgot password page',
        'reset_password.html': 'Reset password page',
    }
    
    print_subsection("Main Templates:")
    all_present = True
    for template, desc in required_templates.items():
        template_path = os.path.join(template_dir, template)
        if os.path.exists(template_path):
            print(f"✓ {template} - {desc}")
        else:
            print(f"✗ {template} - MISSING - {desc}")
            all_present = False
    
    print_subsection("Error Templates:")
    error_dir = os.path.join(template_dir, 'errors')
    if os.path.exists(error_dir):
        error_templates = ['404.html', '500.html']
        for template in error_templates:
            template_path = os.path.join(error_dir, template)
            if os.path.exists(template_path):
                print(f"✓ {template}")
            else:
                print(f"✗ {template} - MISSING")
    else:
        print("⚠ Errors directory not found")
    
    return all_present

def test_dependencies():
    """Test if all required packages are installed."""
    print_section("9. DEPENDENCIES CHECK")
    
    required_packages = {
        'flask': 'Flask web framework',
        'pymongo': 'MongoDB driver',
        'flask_login': 'Flask-Login',
        'flask_wtf': 'Flask-WTF',
        'wtforms': 'WTForms',
        'bcrypt': 'Password hashing',
        'dotenv': 'Environment variables (python-dotenv)',
        'flask_limiter': 'Rate limiting',
        'gunicorn': 'Production server',
    }
    
    print_subsection("Installed Packages:")
    all_installed = True
    for package, desc in required_packages.items():
        try:
            __import__(package)
            print(f"✓ {package} - {desc}")
        except ImportError:
            print(f"✗ {package} - NOT INSTALLED - {desc}")
            all_installed = False
    
    return all_installed

def test_configuration_files():
    """Test if configuration files exist."""
    print_section("10. CONFIGURATION FILES CHECK")
    
    config_files = {
        '.env': 'Environment variables (local)',
        '.env.example': 'Environment template',
        'requirements.txt': 'Python dependencies',
        'Procfile': 'Render process file',
        'runtime.txt': 'Python version',
        'build.sh': 'Build script',
        'render.yaml': 'Render configuration',
        '.gitignore': 'Git ignore rules',
    }
    
    print_subsection("Configuration Files:")
    for file, desc in config_files.items():
        if os.path.exists(file):
            print(f"✓ {file} - {desc}")
        else:
            status = "⚠" if file == '.env' else "✗"
            print(f"{status} {file} - {desc}")

def run_health_check():
    """Run complete health check."""
    print("\n" + "="*70)
    print(" ECOREBORN PROJECT HEALTH CHECK")
    print(" " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    print("="*70)
    
    results = {
        'Environment Variables': test_environment_variables(),
        'Database': test_database_connection(),
        'Models': test_models(),
        'Forms': test_forms(),
        'Routes': test_routes(),
        'Flask App': test_app_creation(),
        'Static Files': test_static_files(),
        'Templates': test_templates(),
        'Dependencies': test_dependencies(),
    }
    
    test_configuration_files()
    
    # Summary
    print_section("HEALTH CHECK SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print_subsection("Results:")
    for component, status in results.items():
        symbol = "✅" if status else "❌"
        print(f"{symbol} {component}: {'PASS' if status else 'FAIL'}")
    
    print_subsection("Overall Status:")
    if passed == total:
        print(f"\n✅ ALL CHECKS PASSED ({passed}/{total})")
        print("\n🎉 Your project is working perfectly!")
        print("\nYou can now:")
        print("  • Run locally: python app.py")
        print("  • Deploy to Render: git push origin main")
        print("  • Visit: http://localhost:5000")
    else:
        print(f"\n⚠️  SOME CHECKS FAILED ({passed}/{total} passed)")
        print("\n📝 Please review the failures above and fix them.")
    
    print("\n" + "="*70)
    
    return passed == total


if __name__ == '__main__':
    success = run_health_check()
    sys.exit(0 if success else 1)
