"""
AgriSense AI — Production Application Entrypoint
Boots the FastAPI high-performance ASGI server serving:
- React 18 Mobile Single-Page Application (Vite bundle at / and /dashboard)
- Modbus RS485 & IoT Sensor Telemetry (/sensor/data)
- Random Forest ML Crop Recommendation (/predict/crop)
- Multilingual Daily 1-Minute Spoken Audio Briefings (/farm/daily-briefing)
- Google Gemini Live WebSockets & Vision AI (/live & /ai/diagnose)
"""

import os
import sys

# Ensure UTF-8 output on all operating systems
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

import uvicorn

port = int(os.environ.get("PORT", 8000))
host = "0.0.0.0"

def start_server():
    print(f"===========================================================")
    print(f"🌱 AgriSense AI — Production Server Launching")
    print(f"⚡ Binding host: {host}:{port}")
    print(f"📱 Frontend: React 18 Mobile SPA (Vite Production Build)")
    print(f"🌾 Backend: FastAPI + SQLite WAL + Random Forest ML")
    print(f"===========================================================")
    uvicorn.run("server:app", host=host, port=port, log_level="info")

if __name__ == "__main__":
    start_server()