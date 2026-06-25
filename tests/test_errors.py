# tests/test_errors.py
import requests
import os

BASE = "http://localhost:5000"

print("\n" + "="*50)
print("  ERROR HANDLING TESTS")
print("="*50)

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

# Test 1 — 404 page
print("\n🔍 404 Error Handling")
try:
    r = requests.get(f"{BASE}/nonexistent-page-xyz")
    test("404 returns correct status", r.status_code == 404)
    test("404 page has content",       len(r.text) > 100)
    test("404 shows friendly message", '404' in r.text)
except Exception as e:
    test("404 handler works", False, str(e))

# Test 2 — No file upload
print("\n📁 Empty Upload Handling")
try:
    r = requests.post(
        f"{BASE}/api/predict",
        files={},
        allow_redirects=False
    )
    test("Empty upload handled",
         r.status_code in [400, 302])
except Exception as e:
    test("Empty upload handled", False, str(e))

# Test 3 — Wrong file type
print("\n📄 Wrong File Type Handling")
try:
    fake_txt = ('test.txt', b'this is not an image', 'text/plain')
    r = requests.post(
        f"{BASE}/api/predict",
        files={'file': fake_txt},
        allow_redirects=True
    )
    test("Wrong type handled",
         r.status_code in [400, 200])
except Exception as e:
    test("Wrong type handled", False, str(e))

# Test 4 — Corrupted image
print("\n🖼️  Corrupted Image Handling")
try:
    fake_img = (
        'fake.jpg',
        b'this is not a real jpg file!!!',
        'image/jpeg'
    )
    r = requests.post(
        f"{BASE}/api/predict",
        files={'file': fake_img},
        allow_redirects=True
    )
    test("Corrupted image handled",
         r.status_code in [400, 200])
    test("App didn't crash",
         'Internal Server Error' not in r.text)
except Exception as e:
    test("Corrupted image handled", False, str(e))

# Test 5 — Stats API always works
print("\n📊 API Stability")
try:
    r = requests.get(f"{BASE}/api/stats/json")
    test("Stats API stable",    r.status_code == 200)
    test("Returns valid JSON",  'success' in r.json())
except Exception as e:
    test("API stable", False, str(e))

# Test 6 — History page always works
print("\n📋 Page Stability")
try:
    r = requests.get(f"{BASE}/history")
    test("History page stable", r.status_code == 200)
    r = requests.get(f"{BASE}/upload")
    test("Upload page stable",  r.status_code == 200)
    r = requests.get(f"{BASE}/")
    test("Home page stable",    r.status_code == 200)
except Exception as e:
    test("Pages stable", False, str(e))

# Results
print("\n" + "="*50)
total = passed + failed
pct   = (passed/total*100) if total > 0 else 0
print(f"  RESULTS: {passed}/{total} ({pct:.0f}%)")
print("="*50)

if failed == 0:
    print("\n🎉 ALL ERROR TESTS PASSED!")
else:
    print(f"\n✅ {passed} passed, {failed} need attention")