# flask_app/app.py
# ============================================
# MAIN FLASK APPLICATION
# This is the entry point for our web server
# ============================================

import os
import sys

# Add project root to Python path
# This lets us import from ml/ and flask_app/
sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))

from flask import Flask
from flask_app.database.db import init_database
from flask_app.routes.main import main_bp
from flask_app.routes.api import api_bp

def create_app():
    """
    Application factory function.
    Creates and configures the Flask app.
    """

    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # ── SECRET KEY ───────────────────────────
    # Required for flash messages and sessions
    app.config['SECRET_KEY'] = 'plant-disease-app-secret-2024'

    # ── UPLOAD CONFIGURATION ─────────────────
    app.config['UPLOAD_FOLDER']    = 'flask_app/static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max

    # ── REGISTER BLUEPRINTS ──────────────────
    # Blueprints are groups of routes
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # ── INITIALIZE DATABASE ──────────────────
    with app.app_context():
        init_database()

    # ── URL SUMMARY ──────────────────────────
    print("\n" + "="*50)
    print("  PLANT DISEASE APP - ROUTES")
    print("="*50)
    print("  GET  /              → Home page")
    print("  GET  /upload        → Upload page")
    print("  GET  /result/<id>   → Result page")
    print("  GET  /history       → History page")
    print("  POST /api/predict   → Prediction API")
    print("  POST /api/predict/json → JSON API")
    print("  GET  /api/stats/json   → Statistics")
    print("="*50)

    return app


# ── RUN THE APP ──────────────────────────────
if __name__ == '__main__':
    app = create_app()
    print("\n🌿 Plant Disease Detection App")
    print("🚀 Starting Flask server...")
    print("🌐 Open browser: http://localhost:5000")
    print("   Press Ctrl+C to stop\n")
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )