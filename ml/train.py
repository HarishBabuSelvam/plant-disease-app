# ml/train.py — OPTIMIZED FOR 15 CLASSES
import os, json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, BatchNormalization
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ── CONFIG ──────────────────────────────────────
DATASET_PATH = "dataset/PlantVillage"
MODEL_PATH   = "model/plant_disease_model.h5"
LABELS_PATH  = "model/class_labels.json"
HISTORY_PATH = "model/training_history.png"
IMAGE_SIZE   = 224
BATCH_SIZE   = 32
VAL_SPLIT    = 0.2
# ────────────────────────────────────────────────

print("\n" + "="*55)
print("  PLANT DISEASE TRAINING — OPTIMIZED v3.0")
print("="*55)

# STEP 1 — Classes
classes = sorted([
    d for d in os.listdir(DATASET_PATH)
    if os.path.isdir(os.path.join(DATASET_PATH, d))
])
NUM_CLASSES = len(classes)
print(f"\n✅ Classes: {NUM_CLASSES}")
for i, c in enumerate(classes):
    count = len(os.listdir(os.path.join(DATASET_PATH, c)))
    print(f"   {i:2d} → {c} ({count} images)")

os.makedirs("model", exist_ok=True)
with open(LABELS_PATH, "w") as f:
    json.dump({str(i): c for i, c in enumerate(classes)}, f, indent=4)
print(f"\n✅ Labels saved")

# STEP 2 — Data Generators
print("\n📊 Setting up data generators...")

train_gen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=45,
    width_shift_range=0.3,
    height_shift_range=0.3,
    shear_range=0.2,
    zoom_range=0.3,
    horizontal_flip=True,
    brightness_range=[0.7, 1.3],
    fill_mode='nearest',
    validation_split=VAL_SPLIT
).flow_from_directory(
    DATASET_PATH,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='training',
    shuffle=True,
    seed=42
)

val_gen = ImageDataGenerator(
    rescale=1./255,
    validation_split=VAL_SPLIT
).flow_from_directory(
    DATASET_PATH,
    target_size=(IMAGE_SIZE, IMAGE_SIZE),
    batch_size=BATCH_SIZE,
    class_mode='categorical',
    subset='validation',
    shuffle=False,
    seed=42
)

print(f"✅ Train: {train_gen.samples} | Val: {val_gen.samples}")

# STEP 3 — Build Model
print("\n🧠 Building model...")

base = MobileNetV2(
    weights='imagenet',
    include_top=False,
    input_shape=(IMAGE_SIZE, IMAGE_SIZE, 3)
)
base.trainable = False

x = base.output
x = GlobalAveragePooling2D()(x)
x = BatchNormalization()(x)
x = Dense(512, activation='relu')(x)
x = Dropout(0.5)(x)
x = Dense(256, activation='relu')(x)
x = Dropout(0.3)(x)
out = Dense(NUM_CLASSES, activation='softmax')(x)
model = Model(base.input, out)

print(f"✅ Model ready | Classes: {NUM_CLASSES}")

# STEP 4 — PHASE 1: Train custom layers
print("\n" + "="*55)
print("  PHASE 1: Training top layers (10 epochs)")
print("="*55)

model.compile(
    optimizer=Adam(1e-3),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

cb1 = [
    ModelCheckpoint(MODEL_PATH, monitor='val_accuracy',
                    save_best_only=True, mode='max', verbose=1),
    EarlyStopping(monitor='val_accuracy', patience=5,
                  restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_accuracy', factor=0.3,
                      patience=3, min_lr=1e-7, verbose=1)
]

h1 = model.fit(train_gen, epochs=10,
               validation_data=val_gen,
               callbacks=cb1, verbose=1)

p1_best = max(h1.history['val_accuracy'])
print(f"\n✅ Phase 1 done | Best val accuracy: {p1_best*100:.2f}%")

# STEP 5 — PHASE 2: Fine-tune top layers
print("\n" + "="*55)
print("  PHASE 2: Fine-tuning MobileNetV2 (15 epochs)")
print("="*55)

# Unfreeze top 50 layers for better accuracy
base.trainable = True
for layer in base.layers[:-50]:
    layer.trainable = False

print(f"✅ Unfrozen last 50 layers of MobileNetV2")

model.compile(
    optimizer=Adam(1e-4),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

cb2 = [
    ModelCheckpoint(MODEL_PATH, monitor='val_accuracy',
                    save_best_only=True, mode='max', verbose=1),
    EarlyStopping(monitor='val_accuracy', patience=7,
                  restore_best_weights=True, verbose=1),
    ReduceLROnPlateau(monitor='val_accuracy', factor=0.2,
                      patience=3, min_lr=1e-8, verbose=1)
]

h2 = model.fit(train_gen, epochs=15,
               validation_data=val_gen,
               callbacks=cb2, verbose=1)

p2_best = max(h2.history['val_accuracy'])
print(f"\n✅ Phase 2 done | Best val accuracy: {p2_best*100:.2f}%")

# STEP 6 — Plot & Save
print("\n📈 Saving training graph...")

acc   = h1.history['accuracy']     + h2.history['accuracy']
val   = h1.history['val_accuracy'] + h2.history['val_accuracy']
loss  = h1.history['loss']         + h2.history['loss']
vloss = h1.history['val_loss']     + h2.history['val_loss']
split = len(h1.history['accuracy'])

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Plant Disease Model — Training History', fontsize=14)

ax1.plot(acc,  label='Train',      color='blue',   lw=2)
ax1.plot(val,  label='Validation', color='orange', lw=2)
ax1.axvline(x=split-1, color='red', ls='--', label='Phase 1→2')
ax1.set_title('Accuracy'); ax1.set_xlabel('Epoch')
ax1.legend(); ax1.grid(alpha=0.3)

ax2.plot(loss,  label='Train',      color='blue',   lw=2)
ax2.plot(vloss, label='Validation', color='orange', lw=2)
ax2.axvline(x=split-1, color='red', ls='--', label='Phase 1→2')
ax2.set_title('Loss'); ax2.set_xlabel('Epoch')
ax2.legend(); ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(HISTORY_PATH, dpi=100)
print(f"✅ Graph saved: {HISTORY_PATH}")

# STEP 7 — Final Results
best = max(p1_best, p2_best)
print("\n" + "="*55)
print("  TRAINING COMPLETE!")
print("="*55)
print(f"\n📊 Phase 1 best: {p1_best*100:.2f}%")
print(f"📊 Phase 2 best: {p2_best*100:.2f}%")
print(f"🏆 Overall best: {best*100:.2f}%")
print(f"💾 Model saved:  {MODEL_PATH}")

if best >= 0.85:
    print(f"\n🎉 EXCELLENT! Target achieved!")
elif best >= 0.70:
    print(f"\n✅ GOOD accuracy — app will work well!")
else:
    print(f"\n⚠️  Will improve in next run!")

print("\n✅ Ready for Phase 6!")