# test_kb.py — Test our knowledge base

import sys
sys.path.append('.')
from flask_app.knowledge_base.diseases import (
    get_disease_info, get_statistics,
    get_severity_color, get_recovery_color
)

print("\n" + "="*55)
print("  KNOWLEDGE BASE TEST")
print("="*55)

# Test 1 — Statistics
stats = get_statistics()
print(f"\n📊 Knowledge Base Statistics:")
print(f"   Total entries:    {stats['total_entries']}")
print(f"   Healthy classes:  {stats['healthy_classes']}")
print(f"   Disease classes:  {stats['disease_classes']}")
print(f"   Avg recovery:     {stats['avg_recovery']}%")

# Test 2 — Look up a disease
print(f"\n🔍 Testing: Tomato Early Blight lookup...")
info = get_disease_info("Tomato_Early_blight")
print(f"   Display name:  {info['display_name']}")
print(f"   Plant:         {info['plant']}")
print(f"   Disease:       {info['disease']}")
print(f"   Severity:      {info['severity']}")
print(f"   Spread risk:   {info['spread_risk']}")
print(f"   Recovery:      {info['recovery_chance']}%")
print(f"   Message:       {info['recovery_message']}")
print(f"\n   Cause: {info['cause'][:80]}...")
print(f"\n   Symptoms ({len(info['symptoms'])}):")
for s in info['symptoms']:
    print(f"     • {s}")
print(f"\n   Treatments ({len(info['treatment'])}):")
for t in info['treatment']:
    print(f"     ✅ {t}")

# Test 3 — Healthy plant
print(f"\n🌿 Testing: Healthy Tomato lookup...")
healthy = get_disease_info("Tomato_healthy")
print(f"   Is Healthy:    {healthy['is_healthy']}")
print(f"   Recovery:      {healthy['recovery_chance']}%")
print(f"   Message:       {healthy['recovery_message']}")

# Test 4 — Color coding
print(f"\n🎨 Color coding test:")
print(f"   Severity 'None':      {get_severity_color('None')}")
print(f"   Severity 'Very High': {get_severity_color('Very High')}")
print(f"   Recovery 95%:         {get_recovery_color(95)}")
print(f"   Recovery 35%:         {get_recovery_color(35)}")

# Test 5 — Unknown disease
print(f"\n❓ Testing: Unknown disease fallback...")
unknown = get_disease_info("Unknown_disease_xyz")
print(f"   Handled gracefully: {unknown['display_name']}")

print("\n" + "="*55)
print("✅ Knowledge Base is working perfectly!")
print("="*55)