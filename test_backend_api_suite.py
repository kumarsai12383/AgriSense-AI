import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fastapi.testclient import TestClient
from server import app
from database.farmers import get_or_create_farmer


def run_backend_test_suite():
    print("=" * 60)
    print("AGRISENSE AI — FULL FASTAPI BACKEND TEST SUITE")
    print("=" * 60)

    client = TestClient(app)

    # 1. Setup Test Farmer
    farmer = get_or_create_farmer("Backend Test Farmer", "9876598765")
    fid = farmer["id"]
    print(f"[OK] Farmer verified: ID={fid}, Name={farmer['name']}")

    # 2. GET / (Root / Dashboard)
    res = client.get("/")
    assert res.status_code == 200, f"GET / failed: {res.status_code}"
    print("[PASS] GET / (Root landing / React Dashboard)")

    # 3. GET /dashboard
    res = client.get("/dashboard")
    assert res.status_code == 200, f"GET /dashboard failed: {res.status_code}"
    print("[PASS] GET /dashboard")

    # 4. GET /voice-chat
    res = client.get("/voice-chat")
    assert res.status_code == 200, f"GET /voice-chat failed: {res.status_code}"
    print("[PASS] GET /voice-chat")

    # 5. GET /health
    res = client.get("/health")
    assert res.status_code == 200, f"GET /health failed: {res.status_code}"
    health_data = res.json()
    assert health_data.get("status") == "healthy"
    print(f"[PASS] GET /health (DB Health: {health_data['database']['status']})")

    # 6. POST /sensor/data (IoT stream)
    payload = {
        "farmer_id": fid,
        "nitrogen": 88.0,
        "phosphorus": 45.0,
        "potassium": 48.0,
        "ph": 6.7,
        "temperature": 26.5,
        "humidity": 82.0,
        "rainfall": 180.0,
        "soil_moisture": 38.0,
        "source": "iot"
    }
    res = client.post("/sensor/data", json=payload)
    assert res.status_code == 200, f"POST /sensor/data failed: {res.status_code}"
    print("[PASS] POST /sensor/data (IoT telemetry ingested)")

    # 7. GET /farm/latest/{farmer_id}
    res = client.get(f"/farm/latest/{fid}")
    assert res.status_code == 200, f"GET /farm/latest failed: {res.status_code}"
    reading = res.json().get("data")
    assert reading is not None and reading["nitrogen"] == 88.0
    print(f"[PASS] GET /farm/latest/{fid} (Verified reading: N={reading['nitrogen']})")

    # 8. GET /farm/history/{farmer_id}
    res = client.get(f"/farm/history/{fid}")
    assert res.status_code == 200, f"GET /farm/history failed: {res.status_code}"
    history = res.json().get("data", [])
    assert len(history) >= 1
    print(f"[PASS] GET /farm/history/{fid} (Verified {len(history)} records)")

    # 9. POST /farm/manual
    manual_data = {
        "farmer_id": fid,
        "nitrogen": 92.0,
        "phosphorus": 40.0,
        "potassium": 40.0,
        "ph": 6.4,
        "temperature": 28.0,
        "humidity": 75.0,
        "rainfall": 150.0,
        "soil_moisture": 32.0,
        "source": "manual"
    }
    res = client.post("/farm/manual", json=manual_data)
    assert res.status_code == 200, f"POST /farm/manual failed: {res.status_code}"
    print("[PASS] POST /farm/manual (Manual reading saved)")

    # 10. GET /sensor/status/{farmer_id}
    res = client.get(f"/sensor/status/{fid}")
    assert res.status_code == 200, f"GET /sensor/status failed: {res.status_code}"
    print(f"[PASS] GET /sensor/status/{fid} (Sensor connected: {res.json().get('connected')})")

    # 11. POST /crop/predict
    pred_payload = {
        "farmer_id": fid,
        "nitrogen": 90.0,
        "phosphorus": 42.0,
        "potassium": 43.0,
        "temperature": 25.0,
        "humidity": 80.0,
        "ph": 6.5,
        "rainfall": 220.0
    }
    res = client.post("/crop/predict", json=pred_payload)
    assert res.status_code == 200, f"POST /crop/predict failed: {res.status_code}"
    crop_res = res.json()
    assert "crop" in crop_res
    print(f"[PASS] POST /crop/predict (ML Prediction: '{crop_res['crop']}')")

    # 12. POST /crop/predict-latest/{farmer_id}
    res = client.post(f"/crop/predict-latest/{fid}")
    assert res.status_code == 200, f"POST /crop/predict-latest failed: {res.status_code}"
    pred_latest = res.json()
    assert "crop" in pred_latest
    print(f"[PASS] POST /crop/predict-latest/{fid} (Predicted crop: '{pred_latest['crop']}')")

    # 13. GET /crop/latest/{farmer_id}
    res = client.get(f"/crop/latest/{fid}")
    assert res.status_code == 200, f"GET /crop/latest failed: {res.status_code}"
    latest_crop_data = res.json().get("data", {})
    assert "crop" in latest_crop_data
    print(f"[PASS] GET /crop/latest/{fid} (Verified latest predicted crop: '{latest_crop_data['crop']}')")

    print("=" * 60)
    print("ALL 12 BACKEND FASTAPI ENDPOINTS & LOGIC PASSED 100%!")
    print("=" * 60)


if __name__ == "__main__":
    run_backend_test_suite()
