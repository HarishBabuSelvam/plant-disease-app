# ml/batch_test.py
# Tests predictor on multiple images
# and shows overall accuracy

import os
import sys
sys.path.append('.')
from ml.predict import PlantDiseasePredictor

DATASET_PATH = "dataset/PlantVillage"
IMAGES_PER_CLASS = 5  # Test 5 images per class

print("\n" + "="*55)
print("  BATCH PREDICTION TEST")
print("="*55)

predictor = PlantDiseasePredictor()

correct = 0
total   = 0
results = []

classes = sorted([
    d for d in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, d))
])

print(f"\nTesting {IMAGES_PER_CLASS} images per class...")
print(f"Total classes: {len(classes)}")
print("-"*55)

for class_name in classes:
    class_path = os.path.join(DATASET_PATH, class_name)
    images = [
        f for f in os.listdir(class_path)
        if f.lower().endswith(('.jpg','.jpeg','.png'))
    ][:IMAGES_PER_CLASS]

    class_correct = 0
    for img_file in images:
        img_path = os.path.join(class_path, img_file)
        try:
            result = predictor.predict(img_path)
            is_correct = result['class_name'] == class_name
            if is_correct:
                correct += 1
                class_correct += 1
            total += 1
        except Exception as e:
            print(f"  ❌ Error: {e}")

    acc = (class_correct / len(images) * 100) if images else 0
    status = "✅" if acc >= 80 else "⚠️ "
    print(f"{status} {class_name:<45} {acc:5.1f}%")

print("-"*55)
overall = (correct / total * 100) if total > 0 else 0
print(f"\n🏆 OVERALL ACCURACY: {correct}/{total} = {overall:.1f}%")

if overall >= 90:
    print("🎉 EXCELLENT! Model is performing great!")
elif overall >= 80:
    print("✅ GOOD! Model is working well!")
else:
    print("⚠️  Model needs improvement.")