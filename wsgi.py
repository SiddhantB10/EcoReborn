"""
WSGI entry point for Vercel deployment
"""
from app import app

# Vercel looks for an 'app' object
application = app

if __name__ == "__main__":
    app.run()
