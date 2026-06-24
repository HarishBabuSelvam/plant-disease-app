# ml/predict.py
# ============================================
# PLANT DISEASE PREDICTION PIPELINE
# ============================================
# This module handles everything needed to:
# 1. Load a trained model
# 2. Preprocess any input image
# 3. Run prediction
# 4. Return disease name + confidence
# ============================================

import os
import json
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf

# ── CONFIGURATION ───────────────────────────
MODEL_PATH  = "model/plant_disease_model.h5"
LABELS_PATH = "model/class_labels.json"
IMAGE_SIZE  = 224
# ────────────────────────────────────────────


class PlantDiseasePredictor:
    """
    A class that handles all prediction logic.
    
    Why a class? Because we load the model ONCE
    and reuse it for every prediction. Loading a
    model takes ~3 seconds. If we loaded it every
    time someone uploads an image, the app would
    be very slow!
    """

    def __init__(self):
        """Initialize: load model and labels once"""
        self.model = None
        self.labels = None
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        """Load the trained model and class labels"""
        print("🔄 Loading plant disease model...")

        # Check model file exists
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}\n"
                f"Please run ml/train.py first!"
            )

        # Check labels file exists
        if not os.path.exists(LABELS_PATH):
            raise FileNotFoundError(
                f"Labels not found: {LABELS_PATH}\n"
                f"Please run save_labels.py first!"
            )

        # Load the trained model
        self.model = tf.keras.models.load_model(MODEL_PATH)

        # Load class labels
        with open(LABELS_PATH, "r") as f:
            self.labels = json.load(f)

        self.is_loaded = True
        print(f"✅ Model loaded successfully!")
        print(f"   Classes: {len(self.labels)}")
        print(f"   Input shape: {self.model.input_shape}")

    def preprocess_image(self, image_input):
        """
        Preprocess image for model prediction.
        
        Accepts:
        - File path (string): "path/to/image.jpg"
        - PIL Image object
        - NumPy array
        
        Returns:
        - Preprocessed numpy array ready for model
        """

        # ── HANDLE DIFFERENT INPUT TYPES ────────
        if isinstance(image_input, str):
            # Input is a file path
            if not os.path.exists(image_input):
                raise FileNotFoundError(f"Image not found: {image_input}")

            # Read with OpenCV
            img = cv2.imread(image_input)
            if img is None:
                raise ValueError(f"Could not read image: {image_input}")

            # OpenCV reads as BGR, convert to RGB
            # (Models trained on RGB, OpenCV uses BGR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        elif isinstance(image_input, Image.Image):
            # Input is a PIL Image
            img = np.array(image_input.convert('RGB'))

        elif isinstance(image_input, np.ndarray):
            # Input is already a numpy array
            img = image_input
            if len(img.shape) == 2:
                # Grayscale → convert to RGB
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

        else:
            raise TypeError(f"Unsupported image type: {type(image_input)}")

        # ── RESIZE ──────────────────────────────
        # Resize to exactly 224×224 (model requirement)
        img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))

        # ── NORMALIZE ───────────────────────────
        # Convert pixel values from 0-255 to 0.0-1.0
        img = img.astype(np.float32) / 255.0

        # ── ADD BATCH DIMENSION ─────────────────
        # Model expects shape: (batch_size, 224, 224, 3)
        # Single image shape:  (224, 224, 3)
        # After expand_dims:   (1, 224, 224, 3)
        img = np.expand_dims(img, axis=0)

        return img

    def predict(self, image_input):
        """
        Main prediction function.
        
        Args:
            image_input: file path, PIL image, or numpy array
            
        Returns:
            dict with prediction results:
            {
                'class_index': 6,
                'class_name': 'Tomato_Early_blight',
                'confidence': 94.3,
                'top3': [
                    {'class': 'Tomato_Early_blight', 'confidence': 94.3},
                    {'class': 'Tomato_Late_blight',  'confidence': 3.2},
                    {'class': 'Tomato_Leaf_Mold',    'confidence': 1.1}
                ],
                'is_healthy': False,
                'plant_name': 'Tomato',
                'disease_name': 'Early Blight'
            }
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded!")

        # Step 1: Preprocess the image
        processed = self.preprocess_image(image_input)

        # Step 2: Run model prediction
        # Returns array of shape (1, 15) with probabilities
        predictions = self.model.predict(processed, verbose=0)

        # Step 3: Get the probabilities for this image
        # predictions[0] removes the batch dimension
        probs = predictions[0]

        # Step 4: Find the winning class
        class_index = int(np.argmax(probs))
        confidence  = float(probs[class_index]) * 100

        # Step 5: Get class name from labels
        class_name = self.labels[str(class_index)]

        # Step 6: Get top 3 predictions
        top3_indices = np.argsort(probs)[::-1][:3]
        top3 = [
            {
                'class': self.labels[str(i)],
                'confidence': round(float(probs[i]) * 100, 2)
            }
            for i in top3_indices
        ]

        # Step 7: Parse plant name and disease name
        # Class names look like: "Tomato_Early_blight"
        # or "Tomato__Tomato_mosaic_virus"
        plant_name, disease_name = self._parse_class_name(class_name)

        # Step 8: Check if healthy
        is_healthy = 'healthy' in class_name.lower()

        return {
            'class_index':  class_index,
            'class_name':   class_name,
            'confidence':   round(confidence, 2),
            'top3':         top3,
            'is_healthy':   is_healthy,
            'plant_name':   plant_name,
            'disease_name': disease_name
        }

    def _parse_class_name(self, class_name):
        """
        Parse class name into plant and disease parts.
        
        Examples:
        'Tomato_Early_blight'     → ('Tomato', 'Early Blight')
        'Tomato__Tomato_mosaic_virus' → ('Tomato', 'Mosaic Virus')
        'Pepper__bell___healthy'  → ('Pepper Bell', 'Healthy')
        'Potato__healthy'         → ('Potato', 'Healthy')
        """
        # Clean up the name
        name = class_name.replace('___', '__').replace('__', '_')
        parts = name.split('_')

        if len(parts) >= 2:
            plant   = parts[0].capitalize()
            disease = ' '.join(parts[1:]).replace('_', ' ').title()
        else:
            plant   = class_name
            disease = 'Unknown'

        return plant, disease


# ============================================
# STANDALONE TESTING
# Run: python ml/predict.py
# ============================================
def test_predictor():
    """Test the predictor with a sample image from dataset"""

    print("\n" + "="*55)
    print("  PREDICTION PIPELINE TEST")
    print("="*55)

    # Initialize predictor
    predictor = PlantDiseasePredictor()

    # Find a test image from dataset
    DATASET_PATH = "dataset/PlantVillage"
    test_image   = None
    test_class   = None

    # Pick first image from first class folder
    for class_folder in sorted(os.listdir(DATASET_PATH)):
        class_path = os.path.join(DATASET_PATH, class_folder)
        if os.path.isdir(class_path):
            images = [
                f for f in os.listdir(class_path)
                if f.lower().endswith(('.jpg', '.jpeg', '.png'))
            ]
            if images:
                test_image = os.path.join(class_path, images[0])
                test_class = class_folder
                break

    if not test_image:
        print("❌ No test image found in dataset!")
        return

    print(f"\n🖼️  Test image:    {test_image}")
    print(f"📋 True class:    {test_class}")

    # Run prediction
    print("\n⏳ Running prediction...")
    result = predictor.predict(test_image)

    # Display results
    print("\n" + "="*55)
    print("  PREDICTION RESULTS")
    print("="*55)
    print(f"\n🌿 Plant:         {result['plant_name']}")
    print(f"🦠 Disease:       {result['disease_name']}")
    print(f"📊 Confidence:    {result['confidence']}%")
    print(f"✅ Is Healthy:    {result['is_healthy']}")
    print(f"🏷️  Class Name:    {result['class_name']}")

    print(f"\n📊 TOP 3 PREDICTIONS:")
    print("-"*45)
    for i, pred in enumerate(result['top3'], 1):
        bar_len = int(pred['confidence'] / 2)
        bar     = "█" * bar_len
        print(f"  {i}. {pred['class']:<40}")
        print(f"     {bar} {pred['confidence']}%")

    # Check if prediction matches true class
    print("\n" + "="*55)
    if result['class_name'] == test_class:
        print("✅ CORRECT PREDICTION!")
    else:
        print(f"⚠️  Predicted: {result['class_name']}")
        print(f"   Actual:    {test_class}")
    print("="*55)

    return result


if __name__ == "__main__":
    test_predictor()