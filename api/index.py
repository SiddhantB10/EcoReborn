"""
Vercel serverless entry point for EcoReborn Flask Application.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
except Exception as e:
    # If import fails, create a minimal error-reporting app
    from flask import Flask, jsonify
    app = Flask(__name__)
    
    @app.route('/')
    def error():
        return jsonify({
            'error': 'Failed to import app',
            'message': str(e),
            'path': sys.path
        }), 500

# Export app for Vercel
# Vercel's Python runtime will use this app object
