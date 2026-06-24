# flask_app/routes/api.py
# ============================================
# PREDICTION API
# Handles image upload and ML prediction
# ============================================

import os
import uuid
from flask import (
    Blueprint, request, jsonify,
    redirect, url_for, current_app
)
from werkzeug.utils import secure_filename
from ml.predict import PlantDiseasePredictor
from flask_app.knowledge_base.diseases import get_disease_info
from flask_app.database.db import save_prediction

# ── CONFIGURATION ───────────────────────────
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE_MB   = 10
UPLOAD_FOLDER      = 'flask_app/static/uploads'
# ────────────────────────────────────────────

api_bp = Blueprint('api', __name__)

# Initialize predictor ONCE when app starts
# This loads the ML model into memory once
# and reuses it for every prediction
predictor = None

def get_predictor():
    """Get or create the predictor instance"""
    global predictor
    if predictor is None:
        predictor = PlantDiseasePredictor()
    return predictor


def allowed_file(filename):
    """Check if uploaded file has an allowed extension"""
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def validate_upload(file):
    """
    Validate uploaded file.
    Returns (is_valid, error_message)
    """
    # Check file was selected
    if not file or file.filename == '':
        return False, "No file selected. Please choose an image."

    # Check file extension
    if not allowed_file(file.filename):
        return False, "Invalid file type. Please upload JPG, PNG, or WEBP."

    # Check file size (read first 11MB to check)
    file.seek(0, 2)  # Seek to end
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)     # Reset to beginning

    if size_mb > MAX_FILE_SIZE_MB:
        return False, f"File too large ({size_mb:.1f}MB). Maximum is {MAX_FILE_SIZE_MB}MB."

    return True, None


@api_bp.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint.
    
    Accepts: POST request with image file
    Returns: Redirect to result page
    
    Flow:
    1. Receive uploaded image
    2. Validate the file
    3. Save to uploads folder
    4. Run ML prediction
    5. Get disease info from knowledge base
    6. Save to database
    7. Redirect to result page
    """

    # ── STEP 1: Get uploaded file ────────────
    if 'file' not in request.files:
        return jsonify({
            'error': 'No file in request'
        }), 400

    file = request.files['file']

    # ── STEP 2: Validate file ────────────────
    is_valid, error_msg = validate_upload(file)
    if not is_valid:
        return jsonify({'error': error_msg}), 400

    # ── STEP 3: Save file securely ───────────
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Generate unique filename to avoid conflicts
    # e.g. "leaf.jpg" → "a3f9b2c1-leaf.jpg"
    original_name = secure_filename(file.filename)
    unique_id     = str(uuid.uuid4())[:8]
    ext           = original_name.rsplit('.', 1)[1].lower()
    filename      = f"{unique_id}_{original_name}"
    filepath      = os.path.join(UPLOAD_FOLDER, filename)

    file.save(filepath)

    # ── STEP 4: Run ML prediction ────────────
    try:
        pred   = get_predictor()
        result = pred.predict(filepath)
    except Exception as e:
        # Clean up uploaded file if prediction fails
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({
            'error': f'Prediction failed: {str(e)}'
        }), 500

    # ── STEP 5: Get disease information ──────
    disease_info = get_disease_info(result['class_name'])

    # ── STEP 6: Save to database ─────────────
    prediction_data = {
        'filename':       filename,
        'original_name':  original_name,
        'plant_name':     disease_info['plant'],
        'disease_name':   disease_info['disease'],
        'class_name':     result['class_name'],
        'confidence':     result['confidence'],
        'is_healthy':     result['is_healthy'],
        'severity':       disease_info['severity'],
        'spread_risk':    disease_info['spread_risk'],
        'recovery_chance':disease_info['recovery_chance'],
        'treatment_time': disease_info['treatment_time']
    }

    prediction_id = save_prediction(prediction_data)

    # ── STEP 7: Redirect to result page ──────
    return redirect(
        url_for('main.result', prediction_id=prediction_id)
    )


@api_bp.route('/predict/json', methods=['POST'])
def predict_json():
    """
    JSON prediction endpoint.
    Returns full prediction data as JSON.
    Useful for testing and future mobile apps.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    is_valid, error_msg = validate_upload(file)
    if not is_valid:
        return jsonify({'error': error_msg}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    original_name = secure_filename(file.filename)
    unique_id     = str(uuid.uuid4())[:8]
    filename      = f"{unique_id}_{original_name}"
    filepath      = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        pred         = get_predictor()
        result       = pred.predict(filepath)
        disease_info = get_disease_info(result['class_name'])

        return jsonify({
            'success':      True,
            'prediction': {
                'class_name':     result['class_name'],
                'plant_name':     disease_info['plant'],
                'disease_name':   disease_info['disease'],
                'confidence':     result['confidence'],
                'is_healthy':     result['is_healthy'],
                'top3':           result['top3'],
                'severity':       disease_info['severity'],
                'recovery_chance':disease_info['recovery_chance'],
                'cause':          disease_info['cause'],
                'treatment':      disease_info['treatment'],
                'prevention':     disease_info['prevention']
            }
        })
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': str(e)}), 500


@api_bp.route('/history/json')
def history_json():
    """Returns prediction history as JSON"""
    from flask_app.database.db import get_all_predictions
    predictions = get_all_predictions(limit=20)
    return jsonify({
        'success': True,
        'count': len(predictions),
        'predictions': predictions
    })


@api_bp.route('/stats/json')
def stats_json():
    """Returns app statistics as JSON"""
    from flask_app.database.db import get_statistics
    stats = get_statistics()
    return jsonify({'success': True, 'stats': stats})