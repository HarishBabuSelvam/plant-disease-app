# ml/test_model.py
# Quick check to verify model was saved correctly

import os
import json
import tensorflow as tf

MODEL_PATH = "model/plant_disease_model.h5"
LABELS_PATH = "model/class_labels.json"

print("🔍 Checking saved model...")

# Check model file exists
if os.path.exists(MODEL_PATH):
    size_mb = os.path.getsize(MODEL_PATH) / (1024*1024)
    print(f"✅ Model file found: {MODEL_PATH}")
    print(f"   File size: {size_mb:.1f} MB")
else:
    print(f"❌ Model not found at: {MODEL_PATH}")
    print("   Run train.py first!")
    exit()

# Load the model
print("\n⏳ Loading model...")
model = tf.keras.models.load_model(MODEL_PATH)
print(f"✅ Model loaded successfully!")
print(f"   Input shape:  {model.input_shape}")
print(f"   Output shape: {model.output_shape}")

# Load class labels
with open(LABELS_PATH) as f:
    labels = json.load(f)
print(f"✅ Labels loaded: {len(labels)} classes")

print("\n🎉 Model is ready for predictions!")