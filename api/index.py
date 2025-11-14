"""
Vercel serverless entry point for EcoReborn Flask Application.
This file adapts the Flask app for Vercel's serverless environment.
"""

import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

# Vercel expects the app to be named 'app'
# The Flask app is already created in app.py
