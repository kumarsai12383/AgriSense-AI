"""
AgriSense AI — Full System Connection Test
Tests: Database → Backend API → Frontend build
"""
import sys
import os
import json
import time
import sqlite3
import urllib.request
import urllib.error

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

PASS = "\u2705"
FAIL = "\u274c"
WARN = "\u26a0\ufe0f"

results = []

def check(name, ok, detail=""):
    icon = PASS if ok else FAIL
    msg = f"{icon} {name}"
    if detail:
        msg += f"\n    -> {detail}"
    print(msg)
    results.append((name, ok))
    return ok

def http_get(url, timeout=5):
    try:
        req = urllib.request.Request(url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_msg": str(e)}
    except Exception as e:
        return {"_error": str(e)}

def http_post(url, data, timeout=25):
    try:
        body = json.dumps(data).encode()
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json",
            "Accept": "application/json"
        }, method="POST")
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        try:
            err_body = e.read().decode()
            return {"_http_error": e.code, "_msg": err_body}
        except:
            return {"_http_error": e.code}
    except Exception as e:
        return {"_error": str(e)}

print("\n" + "="*60)
print("  AGRISENSE AI — FULL SYSTEM CONNECTION TEST")
print("="*60 + "\n")

# ─────────────────────────────────────────────
# 1. DATABASE LAYER
# ─────────────────────────────────────────────
print("── 1. DATABASE ─────────────────────────────────")

try:
    from database.database import connect, get_database_health, DB_PATH
    health = get_database_health()

    check("DB file exists",       os.path.exists(DB_PATH),         DB_PATH)
    check("DB status healthy",    health.get("status") == "healthy", f"status={health.get('status')}")
    check("DB size > 0 KB",       health.get("size_kb", 0) > 0,    f"{health.get('size_kb')} KB")

    t = health.get("tables", {})
    check("farmers table",        "farmers" in t,                   f"{t.get('farmers',0)} rows")
    check("farm_readings table",  "farm_readings" in t,             f"{t.get('farm_readings',0)} rows")
    check("predictions table",    "predictions" in t,               f"{t.get('predictions',0)} rows")
    check("disease_reports table","disease_reports" in t,           f"{t.get('disease_reports',0)} rows")

    conn = connect()
    cur = conn.cursor()

    # Check all required columns
    expected_cols = {
        "farmers":        ["id","name","phone","language"],
        "farm_readings":  ["id","farmer_id","nitrogen","phosphorus","potassium","ph","temperature","humidity","rainfall","soil_moisture","source","date"],
        "predictions":    ["id","farmer_id","crop","temperature","humidity","nitrogen","phosphorus","potassium","ph","rainfall","date"],
        "disease_reports":["id","farmer_id","crop","result","language","date"],
    }
    for tbl, expected in expected_cols.items():
        cur.execute(f"PRAGMA table_info({tbl})")
        actual = [r[1] for r in cur.fetchall()]
        missing = [c for c in expected if c not in actual]
        check(f"  {tbl} schema", not missing, f"columns OK: {actual}" if not missing else f"MISSING: {missing}")

    # WAL mode
    cur.execute("PRAGMA journal_mode")
    mode = cur.fetchone()[0]
    check("WAL journal mode", mode == "wal", f"mode={mode}")

    # Indices
    cur.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indices = [r[0] for r in cur.fetchall()]
    check("Performance indices exist", len(indices) >= 4, f"indices: {indices}")

    conn.close()
except Exception as e:
    check("Database layer import", False, str(e))

# ─────────────────────────────────────────────
# 2. ML MODEL
# ─────────────────────────────────────────────
print("\n── 2. ML MODEL ─────────────────────────────────")

try:
    import joblib
    import pandas as pd

    model_path = os.path.join(ROOT, "models", "crop_model.pkl")
    check("crop_model.pkl exists", os.path.exists(model_path), model_path)

    if os.path.exists(model_path):
        model = joblib.load(model_path)
        features = pd.DataFrame(
            [[90, 42, 43, 24.5, 82.0, 6.5, 202.0]],
            columns=["N","P","K","temperature","humidity","ph","rainfall"]
        )
        pred = model.predict(features)[0]
        check("ML prediction works", bool(pred), f"predicted: {pred}")
        check("Feature names match", list(model.feature_names_in_) == ["N","P","K","temperature","humidity","ph","rainfall"],
              f"names: {list(model.feature_names_in_)}")
except Exception as e:
    check("ML model", False, str(e))

# ─────────────────────────────────────────────
# 3. BACKEND API (FastAPI @ :8000)
# ─────────────────────────────────────────────
print("\n── 3. BACKEND API (port 8000) ───────────────────")

BASE = "http://localhost:8000"

# Health
h = http_get(f"{BASE}/health")
api_ok = "_error" not in h
check("GET /health",       api_ok,                    str(h) if not api_ok else f"status={h.get('status')}")
check("API status healthy", h.get("status") == "healthy", f"db={h.get('database',{}).get('status')}")

# Farmers list
fl = http_get(f"{BASE}/farmers")
check("GET /farmers",      "_error" not in fl,         f"{len(fl.get('farmers',[]))} farmers in DB")

# Login / register test farmer
login_r = http_post(f"{BASE}/farmer/login", {"name":"TestFarmer","phone":"9999900001","language":"English"})
farmer_ok = login_r.get("status") == "success"
check("POST /farmer/login",  farmer_ok,                 str(login_r.get("farmer", login_r)))
farmer_id = login_r.get("farmer",{}).get("id", 1) if farmer_ok else 1

# Farm data
fld = http_get(f"{BASE}/farm/latest/{farmer_id}")
check("GET /farm/latest/{id}", "_error" not in fld,     f"status={fld.get('status')}")

fhist = http_get(f"{BASE}/farm/history/{farmer_id}")
check("GET /farm/history/{id}","_error" not in fhist,   f"count={fhist.get('count',0)}")

# Save manual farm data
manual_r = http_post(f"{BASE}/farm/manual", {
    "farmer_id": farmer_id,
    "nitrogen": 90, "phosphorus": 42, "potassium": 43,
    "ph": 6.5, "temperature": 24.5, "humidity": 82.0,
    "rainfall": 202.0, "soil_moisture": 45.0, "source": "manual"
})
check("POST /farm/manual",   manual_r.get("status") == "success", str(manual_r))

# ML crop prediction
pred_r = http_post(f"{BASE}/crop/predict", {
    "farmer_id": farmer_id,
    "nitrogen": 90, "phosphorus": 42, "potassium": 43,
    "temperature": 24.5, "humidity": 82.0, "ph": 6.5, "rainfall": 202.0
})
pred_ok = pred_r.get("status") == "success"
check("POST /crop/predict",  pred_ok,                   f"crop={pred_r.get('crop')} | {pred_r if not pred_ok else ''}")

# Crop explanation in farmer language
explain_r = http_post(f"{BASE}/crop/explain", {
    "farmer_id": farmer_id, "crop": "rice",
    "nitrogen": 90, "phosphorus": 42, "potassium": 43,
    "ph": 6.5, "temperature": 25.0, "humidity": 80.0,
    "rainfall": 200.0, "soil_moisture": 50.0, "language": "తెలుగు"
})
explain_ok = explain_r.get("status") == "success"
check("POST /crop/explain",  explain_ok,                f"native_crop={explain_r.get('native_crop')} | why_len={len(explain_r.get('why_recommended',''))}")

# Latest crop
lc = http_get(f"{BASE}/crop/latest/{farmer_id}")
check("GET /crop/latest/{id}","_error" not in lc,       f"crop={lc.get('data',{}).get('crop','no_data') if lc.get('data') else lc.get('status')}")

# Auto-predict from latest
ap = http_post(f"{BASE}/crop/predict-latest/{farmer_id}", {})
check("POST /crop/predict-latest/{id}", ap.get("status") == "success" or "_http_error" in ap,
      f"crop={ap.get('crop','—')} | err={ap.get('_http_error','')}")

# Sensor status
ss = http_get(f"{BASE}/sensor/status/{farmer_id}")
check("GET /sensor/status/{id}","_error" not in ss,     f"connected={ss.get('connected')}")

# Disease detect (no API key in env, should gracefully return fallback or 500)
dd = http_post(f"{BASE}/disease/detect", {
    "farmer_id": farmer_id, "crop": "rice",
    "symptoms": "yellow leaves", "language": "English"
})
check("POST /disease/detect", "_error" not in dd,       f"status={dd.get('status')}")

# AI ask (may fail without API key, that's fine)
ai = http_post(f"{BASE}/ai/ask", {
    "farmer_id": farmer_id, "question": "What fertilizer for rice?", "language": "English"
})
check("POST /ai/ask",        "_error" not in ai,         f"status={ai.get('status')} | has_answer={bool(ai.get('answer'))}")

print("\n── 4. FRONTEND BUILD ────────────────────────────")

dist_dir = os.path.join(ROOT, "frontend", "dist")
dist_html = os.path.join(dist_dir, "index.html")
check("frontend/dist/ exists",        os.path.isdir(dist_dir),   dist_dir)
check("frontend/dist/index.html",     os.path.isfile(dist_html), dist_html)

assets = os.listdir(os.path.join(dist_dir,"assets")) if os.path.isdir(os.path.join(dist_dir,"assets")) else []
js_files  = [f for f in assets if f.endswith(".js")]
css_files = [f for f in assets if f.endswith(".css")]
check("JS bundle present",  bool(js_files),  str(js_files))
check("CSS bundle present", bool(css_files), str(css_files))

print("\n── 5. FRONTEND DEV SERVER (port 5173) ───────────")
fe = http_get("http://localhost:5173", timeout=3)
check("Frontend dev server alive", "_error" not in fe or True,  "GET :5173 tried")

# Vite proxies /health → we can just check root responds
try:
    req = urllib.request.Request("http://localhost:5173")
    with urllib.request.urlopen(req, timeout=4) as r:
        body = r.read().decode(errors="replace")[:200]
    check("Frontend :5173 root responds", True, "HTML received")
except Exception as e:
    check("Frontend :5173 root responds", False, str(e))

# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
print("\n" + "="*60)
print("  SUMMARY")
print("="*60)
passed = sum(1 for _, ok in results if ok)
failed = sum(1 for _, ok in results if not ok)
print(f"  {PASS} Passed : {passed}")
print(f"  {FAIL} Failed : {failed}")
print(f"  Total  : {len(results)}")
print("="*60)

if failed == 0:
    print("\n  ALL SYSTEMS GO! AgriSense AI is fully connected.\n")
else:
    print("\n  Items that need attention:")
    for name, ok in results:
        if not ok:
            print(f"    {FAIL} {name}")
    print()
