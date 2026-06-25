# flask_app/routes/api.py
# ============================================
# PREDICTION API ROUTES — WITH ERROR HANDLING
# ============================================

import os
import uuid
from flask import (
    Blueprint, request, jsonify,
    redirect, url_for, render_template
)
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_MB        = 10
UPLOAD_FOLDER      = 'flask_app/static/uploads'

api_bp = Blueprint('api', __name__)


def allowed_file(filename):
    """Check if file extension is allowed"""
    return (
        '.' in filename and
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def validate_upload(file):
    """
    Validate uploaded file.
    Returns (is_valid, error_message)
    """
    if not file or file.filename == '':
        return False, "No file selected."

    if not allowed_file(file.filename):
        return False, "Invalid type. Use JPG, PNG or WEBP."

    file.seek(0, 2)
    size_mb = file.tell() / (1024 * 1024)
    file.seek(0)

    if size_mb > MAX_FILE_MB:
        return False, f"File too large ({size_mb:.1f}MB). Max {MAX_FILE_MB}MB."

    return True, None


def render_error(title, message, back_url='/upload'):
    """Render a friendly error page instead of crashing"""
    return render_template(
        'errors/error.html',
        title=title,
        message=message,
        back_url=back_url
    ), 400


# ============================================
# MAIN PREDICT ROUTE
# ============================================
@api_bp.route('/predict', methods=['POST'])
def predict():
    """
    Main prediction endpoint with full error handling.

    Flow:
    1. Receive uploaded image
    2. Validate file type and size
    3. Save to uploads folder
    4. Verify it's a real image
    5. Run ML prediction
    6. Get disease info from knowledge base
    7. Save to database
    8. Redirect to result page
    """

    # ── STEP 1: Check file exists ─────────────
    if 'file' not in request.files:
        return render_error(
            'No File Received',
            'Please select an image file to upload.'
        )

    file = request.files['file']

    # ── STEP 2: Validate file ─────────────────
    is_valid, error = validate_upload(file)
    if not is_valid:
        return render_error('Upload Error', error)

    # ── STEP 3: Save file securely ────────────
    try:
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        original = secure_filename(file.filename)
        uid      = str(uuid.uuid4())[:8]
        filename = f"{uid}_{original}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
    except Exception as e:
        return render_error(
            'File Save Error',
            'Could not save your file. Please try again.'
        )

    # ── STEP 4: Verify real image ─────────────
    try:
        from PIL import Image as PILImage
        with PILImage.open(filepath) as img:
            img.verify()
    except Exception:
        # Clean up bad file
        if os.path.exists(filepath):
            os.remove(filepath)
        return render_error(
            'Invalid Image',
            'The file you uploaded is not a valid image. '
            'Please upload a clear JPG, PNG or WEBP photo '
            'of a plant leaf.'
        )

    # ── STEP 5: Run ML prediction ─────────────
    try:
        from ml.predict import get_predictor
        predictor = get_predictor()
        result    = predictor.predict(filepath)
    except FileNotFoundError as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return render_error(
            'Model Not Found',
            'The AI model file is missing. '
            'Please run ml/train.py first.'
        )
    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return render_error(
            'Prediction Failed',
            f'Could not analyze your image. '
            f'Please try a different photo. '
            f'Error: {str(e)[:80]}'
        )

    # ── STEP 6: Get disease knowledge ─────────
    try:
        from flask_app.knowledge_base.diseases import (
            get_disease_info
        )
        disease_info = get_disease_info(result['class_name'])
    except Exception:
        # Use fallback if knowledge base fails
        disease_info = {
            'plant':           result['plant_name'],
            'disease':         result['disease_name'],
            'severity':        'Unknown',
            'spread_risk':     'Unknown',
            'recovery_chance': 60,
            'treatment_time':  'Consult expert'
        }

    # ── STEP 7: Save to database ──────────────
    try:
        from flask_app.database.db import save_prediction
        prediction_id = save_prediction({
            'filename':        filename,
            'original_name':   original,
            'plant_name':      disease_info.get('plant',
                               result['plant_name']),
            'disease_name':    disease_info.get('disease',
                               result['disease_name']),
            'class_name':      result['class_name'],
            'confidence':      result['confidence'],
            'is_healthy':      result['is_healthy'],
            'severity':        disease_info.get('severity',
                               'Unknown'),
            'spread_risk':     disease_info.get('spread_risk',
                               'Unknown'),
            'recovery_chance': disease_info.get('recovery_chance',
                               60),
            'treatment_time':  disease_info.get('treatment_time',
                               'N/A')
        })
    except Exception as e:
        return render_error(
            'Database Error',
            'Prediction succeeded but could not be saved. '
            'Please try again.'
        )

    # ── STEP 8: Redirect to result page ───────
    return redirect(
        url_for('main.result', prediction_id=prediction_id)
    )


# ============================================
# JSON API ENDPOINT
# ============================================
@api_bp.route('/predict/json', methods=['POST'])
def predict_json():
    """
    JSON prediction endpoint.
    Returns full prediction data as JSON.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']
    is_valid, error = validate_upload(file)
    if not is_valid:
        return jsonify({'error': error}), 400

    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    original = secure_filename(file.filename)
    uid      = str(uuid.uuid4())[:8]
    filename = f"{uid}_{original}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    try:
        # Verify image
        from PIL import Image as PILImage
        with PILImage.open(filepath) as img:
            img.verify()
    except Exception:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({'error': 'Invalid image file'}), 400

    try:
        from ml.predict import get_predictor
        from flask_app.knowledge_base.diseases import (
            get_disease_info
        )
        predictor    = get_predictor()
        result       = predictor.predict(filepath)
        disease_info = get_disease_info(result['class_name'])

        return jsonify({
            'success': True,
            'prediction': {
                'class_name':      result['class_name'],
                'plant_name':      disease_info['plant'],
                'disease_name':    disease_info['disease'],
                'confidence':      result['confidence'],
                'is_healthy':      result['is_healthy'],
                'top3':            result['top3'],
                'severity':        disease_info['severity'],
                'recovery_chance': disease_info['recovery_chance'],
                'cause':           disease_info['cause'],
                'treatment':       disease_info['treatment'],
                'prevention':      disease_info['prevention']
            }
        })

    except Exception as e:
        if os.path.exists(filepath):
            os.remove(filepath)
        return jsonify({
            'error':   'Prediction failed',
            'details': str(e)
        }), 500


# ============================================
# UTILITY API ENDPOINTS
# ============================================
@api_bp.route('/history/json')
def history_json():
    """Returns prediction history as JSON"""
    try:
        from flask_app.database.db import get_all_predictions
        predictions = get_all_predictions(limit=20)
        return jsonify({
            'success': True,
            'count':   len(predictions),
            'data':    predictions
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/stats/json')
def stats_json():
    """Returns app statistics as JSON"""
    try:
        from flask_app.database.db import get_statistics
        return jsonify({
            'success': True,
            'stats':   get_statistics()
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/health')
def health_check():
    """
    Health check endpoint.
    Useful for deployment platforms to verify app is running.
    """
    try:
        from flask_app.database.db import get_statistics
        stats = get_statistics()
        return jsonify({
            'status':      'healthy',
            'database':    'connected',
            'predictions': stats['total']
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error':  str(e)
        }), 500