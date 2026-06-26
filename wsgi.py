# wsgi.py
# Entry point for gunicorn on Render
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask_app.app import create_app

app = create_app()

if __name__ == "__main__":
    app.run()