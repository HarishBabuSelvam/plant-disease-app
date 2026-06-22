# view_samples.py
# Shows sample images from dataset
# so we can visually confirm data looks correct

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import random

DATASET_PATH = "dataset/PlantVillage"

# Pick 9 random classes
classes = sorted(os.listdir(DATASET_PATH))
selected = random.sample(classes, min(9, len(classes)))

# Create a 3x3 grid of images
fig, axes = plt.subplots(3, 3, figsize=(12, 12))
fig.suptitle("PlantVillage Dataset - Sample Images", 
             fontsize=16, fontweight='bold')

for idx, (ax, class_name) in enumerate(zip(axes.flat, selected)):
    class_path = os.path.join(DATASET_PATH, class_name)
    
    # Get random image from this class
    images = [f for f in os.listdir(class_path) 
              if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    if images:
        img_path = os.path.join(class_path, random.choice(images))
        img = mpimg.imread(img_path)
        ax.imshow(img)
        
        # Clean up the class name for display
        display_name = class_name.replace("___", "\n").replace("_", " ")
        ax.set_title(display_name, fontsize=9, pad=5)
    
    ax.axis('off')

plt.tight_layout()
plt.savefig("dataset_samples.png", dpi=100, bbox_inches='tight')
plt.show()
print("✅ Sample images saved as dataset_samples.png")