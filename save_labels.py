# save_labels.py
# Saves class labels to a JSON file
# We'll use this during prediction to convert
# numbers back to disease names

import os
import json

DATASET_PATH = "dataset/PlantVillage"
OUTPUT_PATH = "model/class_labels.json"

# Create model folder if it doesn't exist
os.makedirs("model", exist_ok=True)

# Get sorted class names (sorting ensures consistent ordering)
classes = sorted([
    d for d in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, d))
])

# Create dictionary: number → class name
class_labels = {str(i): name for i, name in enumerate(classes)}

# Save to JSON file
with open(OUTPUT_PATH, "w") as f:
    json.dump(class_labels, f, indent=4)

print(f"✅ Saved {len(classes)} class labels to {OUTPUT_PATH}")
print("\nFirst 5 labels:")
for i in range(min(5, len(classes))):
    print(f"  {i} → {classes[i]}")

print("\nLast 5 labels:")
for i in range(max(0, len(classes)-5), len(classes)):
    print(f"  {i} → {classes[i]}")