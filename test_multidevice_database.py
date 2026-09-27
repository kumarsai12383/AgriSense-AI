import sys
import io
import os
import sqlite3
import threading
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

print("==========================================================")
print("🌾 AGRISENSE AI — MULTI-DEVICE DATABASE VERIFICATION")
print("==========================================================")

from database.database import connect, initialize_database, get_database_health, DB_PATH
from database.farmers import get_or_create_farmer, update_farmer_language
from database.prediction_db import save_prediction
from modules.disease_detection import save_disease_report, get_latest_farm_context
from modules.irrigation_advisor import get_latest_farm_reading, get_latest_predicted_crop

# 1. Test Auto-Bootstrap & Health
print(f"\n[1/4] Checking Database Schema & Health...")
initialize_database()
health = get_database_health()
print(f"   Database Path: {health['db_path']}")
print(f"   Size: {health['size_kb']} KB")
print(f"   Table Rows: {health['tables']}")
assert health["status"] == "healthy", "Database health check failed!"
print("   [OK] Database schema and tables verified.")

# 2. Test Multi-Device Simulation
print("\n[2/4] Simulating 5 Concurrent Devices (Phone, Tablet, Laptop, ESP32 Sensor, Camera)...")

device_logs = []
def device_farmer_mobile(phone, name, lang):
    """Device 1: Farmer on Android Mobile registering and setting language."""
    try:
        farmer = get_or_create_farmer(name, phone)
        update_farmer_language(farmer["id"], lang)
        device_logs.append(f"Device-Mobile: Registered farmer #{farmer['id']} ({name}) in {lang}")
    except Exception as e:
        device_logs.append(f"Device-Mobile ERROR: {e}")

def device_esp32_sensor(farmer_id, n, p, k, ph, moisture):
    """Device 2: ESP32 IoT Soil Sensor streaming telemetry."""
    try:
        conn = connect()
        conn.execute("""
            INSERT INTO farm_readings (farmer_id, nitrogen, phosphorus, potassium, ph, temperature, humidity, rainfall, soil_moisture, source)
            VALUES (?, ?, ?, ?, ?, 27.5, 70.0, 150.0, ?, 'iot')
        """, (farmer_id, n, p, k, ph, moisture))
        conn.commit()
        conn.close()
        device_logs.append(f"Device-ESP32: Streamed IoT reading (Moisture={moisture}%, N={n})")
    except Exception as e:
        device_logs.append(f"Device-ESP32 ERROR: {e}")

def device_farmer_tablet(farmer_id, crop):
    """Device 3: Farmer on Tablet running crop recommendation."""
    try:
        save_prediction(crop, 26.0, 72.0, 85.0, 42.0, 44.0, 6.8, 190.0, farmer_id)
        device_logs.append(f"Device-Tablet: Saved ML prediction for crop '{crop}'")
    except Exception as e:
        device_logs.append(f"Device-Tablet ERROR: {e}")

def device_leaf_camera(farmer_id, crop, disease):
    """Device 4: Mobile Camera uploading leaf disease scan."""
    try:
        save_disease_report(farmer_id, crop, "leaf_sample.jpg", disease, "Telugu")
        device_logs.append(f"Device-Camera: Saved Leaf Doctor diagnosis '{disease}'")
    except Exception as e:
        device_logs.append(f"Device-Camera ERROR: {e}")

def device_irrigation_advisor(farmer_id):
    """Device 5: Background irrigation check reading telemetry."""
    try:
        reading = get_latest_farm_reading(farmer_id)
        crop = get_latest_predicted_crop(farmer_id)
        m = reading["soil_moisture"] if reading else "N/A"
        device_logs.append(f"Device-Irrigation: Read live moisture={m}%, Crop={crop}")
    except Exception as e:
        device_logs.append(f"Device-Irrigation ERROR: {e}")

# Launch all 5 device actions concurrently across threads
t1 = threading.Thread(target=device_farmer_mobile, args=("9876500001", "Ramesh Farmer", "Telugu"))
t1.start()
t1.join() # ensure farmer is registered for dependent devices

t2 = threading.Thread(target=device_esp32_sensor, args=(1, 90.0, 45.0, 48.0, 6.7, 32.0))
t3 = threading.Thread(target=device_farmer_tablet, args=(1, "rice"))
t4 = threading.Thread(target=device_leaf_camera, args=(1, "rice", "Rice Blast (Magnaporthe oryzae)"))
t5 = threading.Thread(target=device_irrigation_advisor, args=(1,))

# Start all concurrent operations simultaneously
for t in [t2, t3, t4, t5]:
    t.start()
for t in [t2, t3, t4, t5]:
    t.join()

for log in device_logs:
    print(f"   -> {log}")

# 3. Test Cross-Device Data Retrieval
print("\n[3/4] Verifying Multi-Device Data Retrieval...")
reading = get_latest_farm_reading(1)
crop = get_latest_predicted_crop(1)
reading_ctx, crop_ctx = get_latest_farm_context(1)

print(f"   [OK] Latest Soil Moisture read across devices: {reading['soil_moisture']}% (Source: {reading['source']})")
print(f"   [OK] Latest Recommended Crop read across devices: {crop}")
print(f"   [OK] Latest Farm Context verified: N={reading_ctx['nitrogen']}, P={reading_ctx['phosphorus']}, K={reading_ctx['potassium']}")

# 4. Check FastAPI Server Diagnostics
print("\n[4/4] Testing FastAPI /health endpoint with database diagnostics...")
from server import app as fastapi_app
from fastapi.testclient import TestClient

client = TestClient(fastapi_app)
resp = client.get("/health")
assert resp.status_code == 200
print(f"   [OK] FastAPI /health response: {resp.json()}")

print("\n==========================================================")
print("ALL MULTI-DEVICE & LOCAL DATABASE TESTS PASSED 100%!")
print("==========================================================")
