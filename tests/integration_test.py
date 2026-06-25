# tests/integration_test.py
# Tests the complete prediction pipeline

import os
import sys
import json
import requests

sys.path.insert(0, '.')

BASE_URL     = "http://localhost:5000"
DATASET_PATH = "dataset/PlantVillage"

print("\n" + "="*55)
print("  INTEGRATION TEST SUITE")
print("="*55)

passed = 0
failed = 0

def test(name, condition, detail=""):
    global passed, failed
    if condition:
        print(f"  ✅ {name}")
        passed += 1
    else:
        print(f"  ❌ {name} {detail}")
        failed += 1

# ── TEST 1: Server Running ────────────────────
print("\n📡 TEST 1: Server Connection")
try:
    r = requests.get(BASE_URL, timeout=5)
    test("Home page accessible", r.status_code == 200)
except Exception as e:
    test("Home page accessible", False, str(e))
    print("   ⚠️  Make sure 'python run.py' is running!")

# ── TEST 2: All Pages Load ────────────────────
print("\n📄 TEST 2: Page Routes")
pages = [
    ('/', 'Home'),
    ('/upload', 'Upload'),
    ('/history', 'History')
]
for path, name in pages:
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=5)
        test(f"{name} page loads (200)", r.status_code == 200)
    except Exception as e:
        test(f"{name} page loads", False, str(e))

# ── TEST 3: API Endpoints ─────────────────────
print("\n🔌 TEST 3: API Endpoints")
try:
    r = requests.get(f"{BASE_URL}/api/stats/json", timeout=5)
    test("Stats API returns 200", r.status_code == 200)
    data = r.json()
    test("Stats has 'success' key", 'success' in data)
    test("Stats has 'stats' key",   'stats' in data)
    test("Stats has 'total' field", 'total' in data.get('stats', {}))
except Exception as e:
    test("Stats API works", False, str(e))

# ── TEST 4: Image Upload & Prediction ─────────
print("\n🖼️  TEST 4: Image Upload & Prediction")

test_image = None
test_class = None

if os.path.exists(DATASET_PATH):
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

if test_image:
    test("Test image found", True, test_image)
    try:
        with open(test_image, 'rb') as f:
            files = {'file': (os.path.basename(test_image),
                              f, 'image/jpeg')}
            r = requests.post(
                f"{BASE_URL}/api/predict",
                files=files,
                allow_redirects=True,
                timeout=30
            )
        test("Upload returns 200",     r.status_code == 200)
        test("Redirected to result",   '/result/' in r.url)
        test("Result page has content",len(r.text) > 500)
    except Exception as e:
        test("Upload works", False, str(e))
else:
    print("  ⚠️  No test image found in dataset")

# ── TEST 5: Database ──────────────────────────
print("\n💾 TEST 5: Database")
try:
    sys.path.insert(0, '.')
    from flask_app.database.db import (
        get_all_predictions, get_statistics
    )
    preds = get_all_predictions()
    stats = get_statistics()
    test("Can read predictions",     isinstance(preds, list))
    test("Can read statistics",      isinstance(stats, dict))
    test("Stats has total field",    'total' in stats)
    test("Prediction saved to DB",   stats['total'] > 0)
except Exception as e:
    test("Database works", False, str(e))

# ── TEST 6: Knowledge Base ────────────────────
print("\n🧠 TEST 6: Knowledge Base")
try:
    from flask_app.knowledge_base.diseases import (
        get_disease_info, get_statistics as kb_stats
    )
    info  = get_disease_info("Tomato_Early_blight")
    stats = kb_stats()
    test("KB lookup works",          'cause' in info)
    test("KB has symptoms",          len(info['symptoms']) > 0)
    test("KB has treatment",         len(info['treatment']) > 0)
    test("KB has recovery chance",   'recovery_chance' in info)
    test(f"KB has {stats['total_entries']} entries",
         stats['total_entries'] >= 15)
except Exception as e:
    test("Knowledge base works", False, str(e))

# ── TEST 7: ML Model ──────────────────────────
print("\n🤖 TEST 7: ML Model")
try:
    from ml.predict import PlantDiseasePredictor
    predictor = PlantDiseasePredictor()
    test("Model loads",         predictor.is_loaded)
    test("Has labels",          len(predictor.labels) > 0)
    test("Correct class count", len(predictor.labels) == 15)
    if test_image:
        result = predictor.predict(test_image)
        test("Prediction runs",      'class_name' in result)
        test("Confidence > 0",       result['confidence'] > 0)
        test("Has top3",             len(result['top3']) == 3)
        test("Has plant_name",       bool(result['plant_name']))
        print(f"\n  🎯 Sample prediction:")
        print(f"     Plant:      {result['plant_name']}")
        print(f"     Disease:    {result['disease_name']}")
        print(f"     Confidence: {result['confidence']}%")
except Exception as e:
    test("ML model works", False, str(e))

# ── FINAL RESULTS ─────────────────────────────
print("\n" + "="*55)
total = passed + failed
pct   = (passed / total * 100) if total > 0 else 0
print(f"  RESULTS: {passed}/{total} tests passed ({pct:.0f}%)")
print("="*55)

if failed == 0:
    print("\n🎉 ALL TESTS PASSED! App is working perfectly!")
elif failed <= 2:
    print(f"\n✅ MOSTLY WORKING! {failed} minor issue(s) to fix.")
else:
    print(f"\n⚠️  {failed} tests failed. Check errors above.")