# flask_app/routes/main.py
# ============================================
# MAIN PAGE ROUTES
# Handles: Home, Upload, Result, History pages
# ============================================

from flask import (
    Blueprint, render_template,
    request, redirect, url_for, flash
)
from flask_app.database.db import (
    get_all_predictions, get_prediction_by_id,
    get_statistics, delete_prediction
)

# Blueprint = a group of related routes
# Think of it as a mini Flask app
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page"""
    stats = get_statistics()
    return render_template('index.html', stats=stats)


@main_bp.route('/upload')
def upload():
    """Upload page"""
    return render_template('upload.html')


@main_bp.route('/result/<int:prediction_id>')
def result(prediction_id):
    """Result page with full disease information"""
    import sys, os
    sys.path.insert(0, os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ))
    from flask_app.knowledge_base.diseases import (
        get_disease_info, get_severity_color, get_recovery_color
    )

    prediction = get_prediction_by_id(prediction_id)

    if not prediction:
        flash('Prediction not found!', 'error')
        return redirect(url_for('main.upload'))

    # Get full disease info from knowledge base
    disease_info = get_disease_info(prediction['class_name'])

    return render_template(
        'result.html',
        prediction=prediction,
        disease_info=disease_info,
        severity_color=get_severity_color(disease_info['severity']),
        recovery_color=get_recovery_color(disease_info['recovery_chance'])
    )


@main_bp.route('/history')
def history():
    """History page — shows all past predictions"""
    predictions = get_all_predictions(limit=50)
    stats       = get_statistics()
    return render_template('history.html',
                           predictions=predictions,
                           stats=stats)


@main_bp.route('/delete/<int:prediction_id>',
               methods=['POST'])
def delete(prediction_id):
    """Delete a prediction from history"""
    delete_prediction(prediction_id)
    flash('Prediction deleted successfully!', 'success')
    return redirect(url_for('main.history'))