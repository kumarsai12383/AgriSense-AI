import requests
import json
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

def run_all_tests():
    base = "http://localhost:8000"
    react = "http://localhost:3000"
    results = {}
    
    print("==================================================")
    print("🌱 AgriSense AI — Complete Project Health & Parity Audit")
    print("==================================================")

    # 1. React Frontend Dev Server
    try:
        r = requests.get(react, timeout=5)
        results["React Dev Server (Port 3000)"] = {
            "status": "PASS" if r.status_code == 200 else "FAIL",
            "code": r.status_code,
            "details": f"Vite Bundle Loaded ({len(r.text)} bytes)"
        }
    except Exception as e:
        results["React Dev Server (Port 3000)"] = {"status": "FAIL", "error": str(e)}

    # 2. FastAPI Backend & SQLite DB Health
    try:
        r = requests.get(f"{base}/health", timeout=5)
        data = r.json()
        results["FastAPI Backend Health (Port 8000)"] = {
            "status": "PASS" if data.get("status") == "healthy" else "DEGRADED",
            "db_tables": data.get("database", {}).get("tables", {})
        }
    except Exception as e:
        results["FastAPI Backend Health (Port 8000)"] = {"status": "FAIL", "error": str(e)}

    # 3. Farmer Authentication & Persistence
    fid = 1
    try:
        payload = {
            "name": "Ramesh Kumar",
            "phone": "9876543210",
            "language": "English",
            "land_size": 2.5,
            "soil_type": "Loamy",
            "state": "Telangana"
        }
        r = requests.post(f"{base}/farmer/login", json=payload, timeout=5)
        data = r.json()
        fid = data.get("farmer", {}).get("id", 1)
        results["Farmer Login & Profile Persistence"] = {
            "status": "PASS" if r.status_code == 200 and data.get("status") == "success" else "FAIL",
            "farmer_id": fid,
            "name": data.get("farmer", {}).get("name")
        }
    except Exception as e:
        results["Farmer Login & Profile Persistence"] = {"status": "FAIL", "error": str(e)}

    # 4. Manual Soil Reading Entry
    try:
        reading = {
            "farmer_id": fid,
            "nitrogen": 88.0,
            "phosphorus": 42.0,
            "potassium": 45.0,
            "temperature": 27.5,
            "humidity": 72.0,
            "ph": 6.8,
            "rainfall": 160.0,
            "soil_moisture": 44.0,
            "source": "manual"
        }
        r = requests.post(f"{base}/farm/manual", json=reading, timeout=5)
        data = r.json()
        results["Manual Farm Reading Logging (/farm/manual)"] = {
            "status": "PASS" if data.get("status") == "success" else "FAIL",
            "reading_id": data.get("reading_id")
        }
    except Exception as e:
        results["Manual Farm Reading Logging (/farm/manual)"] = {"status": "FAIL", "error": str(e)}

    # 5. IoT 7-in-1 Sensor Telemetry Broadcast
    try:
        iot_packet = {
            "farmer_id": fid,
            "nitrogen": 90.0,
            "phosphorus": 40.0,
            "potassium": 44.0,
            "temperature": 28.0,
            "humidity": 65.0,
            "ph": 6.7,
            "rainfall": 150.0,
            "soil_moisture": 32.0,
            "source": "iot"
        }
        r = requests.post(f"{base}/sensor/data", json=iot_packet, timeout=5)
        data = r.json()
        results["IoT Sensor Broadcast (/sensor/data)"] = {
            "status": "PASS" if data.get("status") == "success" else "FAIL",
            "reading_id": data.get("reading_id")
        }
    except Exception as e:
        results["IoT Sensor Broadcast (/sensor/data)"] = {"status": "FAIL", "error": str(e)}

    # 6. Latest Farm Data & Sensor Connection Status
    try:
        r_latest = requests.get(f"{base}/farm/latest/{fid}", timeout=5)
        r_sensor = requests.get(f"{base}/sensor/status/{fid}", timeout=5)
        results["Farm Latest Telemetry & Sensor Status"] = {
            "status": "PASS" if r_latest.status_code == 200 else "FAIL",
            "soil_moisture": r_latest.json().get("data", {}).get("soil_moisture"),
            "sensor_connected": r_sensor.json().get("connected")
        }
    except Exception as e:
        results["Farm Latest Telemetry & Sensor Status"] = {"status": "FAIL", "error": str(e)}

    # 7. ML 7-Factor Crop Predictor
    try:
        crop_req = {
            "farmer_id": fid,
            "nitrogen": 90.0,
            "phosphorus": 42.0,
            "potassium": 43.0,
            "temperature": 26.0,
            "humidity": 80.0,
            "ph": 6.5,
            "rainfall": 200.0
        }
        r = requests.post(f"{base}/crop/predict", json=crop_req, timeout=5)
        data = r.json()
        results["ML Crop Recommendation (/crop/predict)"] = {
            "status": "PASS" if data.get("status") == "success" else "FAIL",
            "predicted_crop": data.get("crop")
        }
    except Exception as e:
        results["ML Crop Recommendation (/crop/predict)"] = {"status": "FAIL", "error": str(e)}

    # 8. AI Agronomist Chat Advisor
    try:
        chat_req = {
            "farmer_id": fid,
            "question": "What is the optimal sowing time for cotton in Telangana?",
            "language": "English"
        }
        r = requests.post(f"{base}/ai/ask", json=chat_req, timeout=12)
        data = r.json()
        results["AI Agronomist Chat (/ai/ask & /ai/chat)"] = {
            "status": "PASS" if data.get("status") == "success" and data.get("answer") else "FAIL",
            "response_length": len(data.get("answer", ""))
        }
    except Exception as e:
        results["AI Agronomist Chat (/ai/ask & /ai/chat)"] = {"status": "FAIL", "error": str(e)}

    # 9. AI Plant Disease Detection
    try:
        disease_req = {
            "farmer_id": fid,
            "crop": "Tomato",
            "symptoms": "Yellowing leaves with concentric rings and brown margins",
            "language": "English"
        }
        r = requests.post(f"{base}/disease/detect", json=disease_req, timeout=12)
        data = r.json()
        results["AI Plant Doctor (/disease/detect)"] = {
            "status": "PASS" if data.get("status") == "success" and data.get("diagnosis") else "FAIL",
            "diagnosis_length": len(data.get("diagnosis", ""))
        }
    except Exception as e:
        results["AI Plant Doctor (/disease/detect)"] = {"status": "FAIL", "error": str(e)}

    # 10. Reading History
    try:
        r = requests.get(f"{base}/farm/history/{fid}?limit=10", timeout=5)
        data = r.json()
        results["Farm History Log (/farm/history)"] = {
            "status": "PASS" if data.get("status") == "success" else "FAIL",
            "records_count": data.get("count", 0)
        }
    except Exception as e:
        results["Farm History Log (/farm/history)"] = {"status": "FAIL", "error": str(e)}

    # Print Summary
    print("\n--- DETAILED AUDIT RESULTS ---")
    for test_name, res in results.items():
        st = res.get("status")
        icon = "✅" if st == "PASS" else "⚠️" if st == "DEGRADED" else "❌"
        print(f"{icon} {test_name}: {st}")
        for k, v in res.items():
            if k != "status":
                print(f"   └─ {k}: {v}")
    print("==================================================")

if __name__ == "__main__":
    run_all_tests()
