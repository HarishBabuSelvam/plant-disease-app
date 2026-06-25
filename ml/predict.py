# ml/predict.py
# ============================================
# PLANT DISEASE PREDICTION PIPELINE
# ============================================

import os
import json
import numpy as np
import cv2
from PIL import Image
import tensorflow as tf

MODEL_PATH  = "model/plant_disease_model.h5"
LABELS_PATH = "model/class_labels.json"
IMAGE_SIZE  = 224


class PlantDiseasePredictor:
    """
    Handles all prediction logic.
    Model is loaded ONCE and reused for every prediction.
    """

    def __init__(self):
        self.model     = None
        self.labels    = None
        self.is_loaded = False
        self._load_model()

    def _load_model(self):
        """Load the trained model and class labels"""
        print("🔄 Loading plant disease model...")

        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model not found: {MODEL_PATH}\n"
                f"Please run ml/train.py first!"
            )

        if not os.path.exists(LABELS_PATH):
            raise FileNotFoundError(
                f"Labels not found: {LABELS_PATH}"
            )

        self.model  = tf.keras.models.load_model(MODEL_PATH)

        with open(LABELS_PATH, "r") as f:
            self.labels = json.load(f)

        self.is_loaded = True
        print(f"✅ Model loaded!")
        print(f"   Classes: {len(self.labels)}")
        print(f"   Input:   {self.model.input_shape}")

    def preprocess_image(self, image_input):
        """
        Preprocess image for model prediction.
        Accepts: file path string, PIL Image, or numpy array
        """

        if isinstance(image_input, str):
            if not os.path.exists(image_input):
                raise FileNotFoundError(
                    f"Image not found: {image_input}"
                )
            img = cv2.imread(image_input)
            if img is None:
                raise ValueError(
                    f"Could not read image: {image_input}"
                )
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        elif isinstance(image_input, Image.Image):
            img = np.array(image_input.convert('RGB'))

        elif isinstance(image_input, np.ndarray):
            img = image_input
            if len(img.shape) == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:
            raise TypeError(
                f"Unsupported type: {type(image_input)}"
            )

        # Resize to 224x224
        img = cv2.resize(img, (IMAGE_SIZE, IMAGE_SIZE))

        # Normalize 0-255 → 0.0-1.0
        img = img.astype(np.float32) / 255.0

        # Add batch dimension (1, 224, 224, 3)
        img = np.expand_dims(img, axis=0)

        return img

    def predict(self, image_input):
        """
        Run prediction on an image.

        Returns dict with:
        - class_name, confidence, top3
        - is_healthy, plant_name, disease_name
        """
        if not self.is_loaded:
            raise RuntimeError("Model not loaded!")

        # Preprocess
        processed = self.preprocess_image(image_input)

        # Predict
        predictions = self.model.predict(processed, verbose=0)
        probs       = predictions[0]

        # Get winner
        class_index = int(np.argmax(probs))
        confidence  = float(probs[class_index]) * 100
        class_name  = self.labels[str(class_index)]

        # Top 3
        top3_indices = np.argsort(probs)[::-1][:3]
        top3 = [
            {
                'class':      self.labels[str(i)],
                'confidence': round(float(probs[i]) * 100, 2)
            }
            for i in top3_indices
        ]

        # Parse names
        plant_name, disease_name = self._parse_class_name(
            class_name
        )

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
        Parse class name into plant and disease.
        e.g. 'Tomato_Early_blight' → ('Tomato','Early Blight')
        """
        name  = class_name.replace('___','_').replace('__','_')
        parts = name.split('_')

        if len(parts) >= 2:
            plant   = parts[0].capitalize()
            disease = ' '.join(parts[1:]).title()
        else:
            plant   = class_name
            disease = 'Unknown'

        return plant, disease


# ── Singleton instance ───────────────────────
_predictor_instance = None

def get_predictor():
    """Get or create singleton predictor"""
    global _predictor_instance
    if _predictor_instance is None:
        _predictor_instance = PlantDiseasePredictor()
    return _predictor_instance


# ── Standalone test ───────────────────────────
if __name__ == "__main__":
    print("\n" + "="*50)
    print("  PREDICTION PIPELINE TEST")
    print("="*50)

    predictor    = PlantDiseasePredictor()
    DATASET_PATH = "dataset/PlantVillage"
    test_image   = None
    test_class   = None

    for cls in sorted(os.listdir(DATASET_PATH)):
        cls_path = os.path.join(DATASET_PATH, cls)
        if os.path.isdir(cls_path):
            imgs = [
                f for f in os.listdir(cls_path)
                if f.lower().endswith(('.jpg','.jpeg','.png'))
            ]
            if imgs:
                test_image = os.path.join(cls_path, imgs[0])
                test_class = cls
                break

    if not test_image:
        print("❌ No test image found!")
    else:
        print(f"\n🖼️  Image: {test_image}")
        print(f"📋 True:  {test_class}")
        print("\n⏳ Predicting...")

        result = predictor.predict(test_image)

        print("\n" + "="*50)
        print("  RESULTS")
        print("="*50)
        print(f"🌿 Plant:      {result['plant_name']}")
        print(f"🦠 Disease:    {result['disease_name']}")
        print(f"📊 Confidence: {result['confidence']}%")
        print(f"✅ Healthy:    {result['is_healthy']}")
        print(f"\n📊 Top 3:")
        for i, p in enumerate(result['top3'], 1):
            bar = '█' * int(p['confidence'] / 2)
            print(f"  {i}. {p['class']}")
            print(f"     {bar} {p['confidence']}%")

        correct = result['class_name'] == test_class
        print(f"\n{'✅ CORRECT!' if correct else '⚠️ Different from true label'}")