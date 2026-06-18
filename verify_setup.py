print("Checking all installations...")
print("-" * 40)

try:
    import flask
    print(f"✅ Flask version: {flask.__version__}")
except ImportError:
    print("❌ Flask NOT installed")

try:
    import tensorflow as tf
    print(f"✅ TensorFlow version: {tf.__version__}")
except ImportError:
    print("❌ TensorFlow NOT installed")

try:
    import cv2
    print(f"✅ OpenCV version: {cv2.__version__}")
except ImportError:
    print("❌ OpenCV NOT installed")

try:
    import numpy as np
    print(f"✅ NumPy version: {np.__version__}")
except ImportError:
    print("❌ NumPy NOT installed")

try:
    import PIL
    print(f"✅ Pillow version: {PIL.__version__}")
except ImportError:
    print("❌ Pillow NOT installed")

try:
    import sklearn
    print(f"✅ Scikit-learn version: {sklearn.__version__}")
except ImportError:
    print("❌ Scikit-learn NOT installed")

try:
    import matplotlib
    print(f"✅ Matplotlib version: {matplotlib.__version__}")
except ImportError:
    print("❌ Matplotlib NOT installed")

print("-" * 40)
print("Verification complete!")