# explore_dataset.py
# This script helps us understand our dataset
# before we start training

import os

# Path to our dataset
DATASET_PATH = "dataset/PlantVillage"

print("=" * 60)
print("         PLANTVILLAGE DATASET EXPLORER")
print("=" * 60)

# Check if dataset exists
if not os.path.exists(DATASET_PATH):
    print("❌ Dataset not found!")
    print(f"   Make sure PlantVillage folder is at: {DATASET_PATH}")
    exit()

# Get all class folders
classes = sorted(os.listdir(DATASET_PATH))
total_images = 0
class_info = []

print(f"\n📁 Total Classes Found: {len(classes)}")
print("-" * 60)
print(f"{'Class Name':<45} {'Images':>10}")
print("-" * 60)

# Count images in each class
for class_name in classes:
    class_path = os.path.join(DATASET_PATH, class_name)
    
    # Only process folders
    if os.path.isdir(class_path):
        # Count image files
        images = [f for f in os.listdir(class_path) 
                  if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        count = len(images)
        total_images += count
        class_info.append((class_name, count))
        print(f"{class_name:<45} {count:>10} images")

print("-" * 60)
print(f"{'TOTAL':<45} {total_images:>10} images")

# Separate healthy vs diseased
print("\n" + "=" * 60)
print("         HEALTHY vs DISEASED BREAKDOWN")
print("=" * 60)

healthy = [(name, count) for name, count in class_info 
           if 'healthy' in name.lower()]
diseased = [(name, count) for name, count in class_info 
            if 'healthy' not in name.lower()]

healthy_total = sum(count for _, count in healthy)
diseased_total = sum(count for _, count in diseased)

print(f"\n✅ Healthy Classes:  {len(healthy)}")
print(f"   Total Images:    {healthy_total}")
print(f"\n🦠 Diseased Classes: {len(diseased)}")
print(f"   Total Images:    {diseased_total}")

# Show plants covered
print("\n" + "=" * 60)
print("         PLANTS COVERED")
print("=" * 60)
plants = set()
for name, _ in class_info:
    plant = name.split("___")[0] if "___" in name else name.split("_")[0]
    plants.add(plant)

for plant in sorted(plants):
    print(f"  🌿 {plant}")

print("\n" + "=" * 60)
print("✅ Dataset exploration complete!")
print("=" * 60)