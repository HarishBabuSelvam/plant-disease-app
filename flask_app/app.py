# flask_app/app.py
# ============================================
# MAIN FLASK APPLICATION — WITH ERROR HANDLING
# ============================================

import os
import sys

sys.path.insert(0, os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
))

from flask import Flask, render_template, jsonify
from flask_app.database.db import init_database
from flask_app.routes.main import main_bp
from flask_app.routes.api import api_bp


def create_app():
    app = Flask(
        __name__,
        template_folder='templates',
        static_folder='static'
    )

    # ── CONFIG ───────────────────────────────
    app.config['SECRET_KEY']         = 'plant-disease-secret-2024'
    app.config['UPLOAD_FOLDER']      = 'flask_app/static/uploads'
    app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB

    # ── BLUEPRINTS ───────────────────────────
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix='/api')

    # ── DATABASE ─────────────────────────────
    with app.app_context():
        init_database()

    # ── ERROR HANDLERS ───────────────────────

    @app.errorhandler(404)
    def not_found(e):
        """Page not found"""
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        """Internal server error"""
        return render_template('errors/500.html'), 500

    @app.errorhandler(413)
    def file_too_large(e):
        """File too large (>10MB)"""
        return render_template('errors/413.html'), 413

    @app.errorhandler(405)
    def method_not_allowed(e):
        """Wrong HTTP method"""
        return render_template('errors/404.html'), 405

    # ── TEMPLATE FILTERS ─────────────────────

    @app.template_filter('severity_color')
    def severity_color(severity):
        colors = {
            'None':      '#28a745',
            'Low':       '#87c944',
            'Medium':    '#ffc107',
            'High':      '#fd7e14',
            'Very High': '#dc3545',
            'Unknown':   '#6c757d'
        }
        return colors.get(severity, '#6c757d')

    @app.template_filter('recovery_color')
    def recovery_color(chance):
        if chance >= 80: return '#28a745'
        if chance >= 60: return '#ffc107'
        if chance >= 40: return '#fd7e14'
        return '#dc3545'

    @app.template_filter('confidence_color')
    def confidence_color(conf):
        if conf >= 90: return '#28a745'
        if conf >= 70: return '#ffc107'
        return '#dc3545'

    # ── ROUTES SUMMARY ───────────────────────
    print("\n" + "="*50)
    print("  PLANT DISEASE APP — ROUTES")
    print("="*50)
    print("  GET  /              → Home")
    print("  GET  /upload        → Upload")
    print("  GET  /result/<id>   → Result")
    print("  GET  /history       → History")
    print("  POST /api/predict   → Predict")
    print("  GET  /api/stats/json→ Stats")
    print("="*50)

    return app


if __name__ == '__main__':
    app = create_app()
    print("\n🌿 Plant Disease Detection App")
    print("🚀 Starting server...")
    print("🌐 Open: http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=True)