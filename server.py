import os
import sys
import asyncio
import sqlite3
from datetime import datetime
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Prevent Windows charmap UnicodeEncodeError when printing emojis
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

from modules.live_context import get_farm_context, get_crop_recommendation


# =========================================================
# CONFIGURATION
# =========================================================

app = FastAPI(
    title="AgriSense AI Backend",
    version="1.0.0",
    description="Central backend for AgriSense AI"
)

# Enable CORS for Streamlit and external clients
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = "gemini-2.5-flash-native-audio-latest"
FALLBACK_LIVE_MODEL = "gemini-3.1-flash-live-preview"
from database.database import connect as get_db_conn, get_database_health, DB_PATH

def get_connection():
    return get_db_conn()


# =========================================================
# REQUEST MODELS
# =========================================================

class FarmReading(BaseModel):
    farmer_id: int

    nitrogen: float | None = None
    phosphorus: float | None = None
    potassium: float | None = None

    ph: float | None = None
    temperature: float | None = None
    humidity: float | None = None
    rainfall: float | None = None
    soil_moisture: float | None = None

    source: str = Field(
        default="manual",
        pattern="^(manual|iot)$"
    )


class CropPredictionRequest(BaseModel):
    farmer_id: int

    nitrogen: float
    phosphorus: float
    potassium: float

    temperature: float
    humidity: float
    ph: float
    rainfall: float


class AIRequest(BaseModel):
    farmer_id: int
    question: str
    language: str = "English"


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/")
def root():
    # If accessed in a web browser, serve the modern React Dashboard directly
    dashboard_path = os.path.join(os.path.dirname(__file__), "static", "react_dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path, media_type="text/html")
    return {
        "name": "AgriSense AI Backend",
        "status": "running",
        "version": "1.0.0",
        "dashboard": "/dashboard",
        "docs": "/docs"
    }


@app.get("/dashboard", response_class=HTMLResponse)
def get_react_dashboard():
    dashboard_path = os.path.join(os.path.dirname(__file__), "static", "react_dashboard.html")
    if os.path.exists(dashboard_path):
        return FileResponse(dashboard_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Dashboard not found")


@app.get("/voice-chat", response_class=HTMLResponse)
def get_voice_chat():
    voice_path = os.path.join(os.path.dirname(__file__), "live_voice_chat.html")
    if os.path.exists(voice_path):
        return FileResponse(voice_path, media_type="text/html")
    raise HTTPException(status_code=404, detail="Voice chat interface not found")


@app.get("/health")
def health():
    db_health = get_database_health()
    return {
        "status": "healthy" if db_health.get("status") == "healthy" else "degraded",
        "service": "AgriSense AI Backend",
        "database": db_health
    }


# =========================================================
# FARMER VALIDATION
# =========================================================

def farmer_exists(farmer_id: int):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT id
            FROM farmers
            WHERE id = ?
            """,
            (farmer_id,)
        )

        return cursor.fetchone() is not None

    finally:
        conn.close()


# =========================================================
# GET LATEST FARM DATA
# =========================================================

def get_latest_farm_reading(farmer_id: int):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                farmer_id,
                nitrogen,
                phosphorus,
                potassium,
                ph,
                temperature,
                humidity,
                rainfall,
                soil_moisture,
                source,
                date
            FROM farm_readings
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (farmer_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return dict(row)

    finally:
        conn.close()


@app.get("/farm/latest/{farmer_id}")
def farm_latest(farmer_id: int):

    if not farmer_exists(farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    reading = get_latest_farm_reading(farmer_id)

    if not reading:
        return {
            "status": "no_data",
            "message": "No farm data has been recorded yet."
        }

    return {
        "status": "success",
        "data": reading
    }


# =========================================================
# FARM HISTORY
# =========================================================

@app.get("/farm/history/{farmer_id}")
def farm_history(
    farmer_id: int,
    limit: int = 50
):

    if not farmer_exists(farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    limit = max(1, min(limit, 200))

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                farmer_id,
                nitrogen,
                phosphorus,
                potassium,
                ph,
                temperature,
                humidity,
                rainfall,
                soil_moisture,
                source,
                date
            FROM farm_readings
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT ?
            """,
            (farmer_id, limit)
        )

        rows = cursor.fetchall()

        return {
            "status": "success",
            "count": len(rows),
            "data": [dict(row) for row in rows]
        }

    finally:
        conn.close()


# =========================================================
# SAVE FARM DATA
# =========================================================

def save_farm_reading(data: FarmReading):

    if not farmer_exists(data.farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO farm_readings (
                farmer_id,
                nitrogen,
                phosphorus,
                potassium,
                ph,
                temperature,
                humidity,
                rainfall,
                soil_moisture,
                source,
                date
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data.farmer_id,
                data.nitrogen,
                data.phosphorus,
                data.potassium,
                data.ph,
                data.temperature,
                data.humidity,
                data.rainfall,
                data.soil_moisture,
                data.source,
                datetime.now().isoformat()
            )
        )

        conn.commit()

        reading_id = cursor.lastrowid

        return reading_id

    finally:
        conn.close()


# =========================================================
# MANUAL FARM DATA
# =========================================================

@app.post("/farm/manual")
def add_manual_farm_data(data: FarmReading):

    data.source = "manual"

    reading_id = save_farm_reading(data)

    return {
        "status": "success",
        "message": "Manual farm data saved successfully.",
        "reading_id": reading_id,
        "source": "manual"
    }


# =========================================================
# IOT SENSOR DATA
# =========================================================

@app.post("/sensor/data")
def receive_sensor_data(data: FarmReading):

    data.source = "iot"

    reading_id = save_farm_reading(data)

    return {
        "status": "success",
        "message": "IoT sensor data received successfully.",
        "reading_id": reading_id,
        "source": "iot"
    }



# =========================================================
# SENSOR STATUS
# =========================================================

@app.get("/sensor/status/{farmer_id}")
def sensor_status(farmer_id: int):
    """
    Report whether the farmer's IoT sensor has recently sent data.

    The mobile app can use this endpoint to show Connected/Offline.
    A sensor is considered connected when its latest IoT reading is
    within the last 10 minutes.
    """
    if not farmer_exists(farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                nitrogen,
                phosphorus,
                potassium,
                ph,
                temperature,
                humidity,
                rainfall,
                soil_moisture,
                source,
                date
            FROM farm_readings
            WHERE farmer_id = ?
              AND source = 'iot'
            ORDER BY id DESC
            LIMIT 1
            """,
            (farmer_id,)
        )

        row = cursor.fetchone()

        if not row:
            return {
                "status": "offline",
                "connected": False,
                "message": "No IoT sensor data has been received yet.",
                "data": None
            }

        reading = dict(row)

        try:
            last_reading_time = datetime.fromisoformat(reading["date"])
            age_seconds = max(
                0,
                (datetime.now() - last_reading_time).total_seconds()
            )
        except (TypeError, ValueError):
            age_seconds = None

        # 10 minutes is a practical default for the first version.
        connected = (
            age_seconds is not None
            and age_seconds <= 600
        )

        return {
            "status": "connected" if connected else "offline",
            "connected": connected,
            "last_seen_seconds": round(age_seconds, 1)
                if age_seconds is not None else None,
            "message": (
                "IoT sensor is connected and sending data."
                if connected
                else "IoT sensor has not sent data recently."
            ),
            "data": reading
        }

    finally:
        conn.close()


# =========================================================
# LATEST CROP RECOMMENDATION
# =========================================================

def get_crop_recommendation(farmer_id):

    conn = get_connection()

    try:

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT
                id,
                crop,
                temperature,
                humidity,
                nitrogen,
                phosphorus,
                potassium,
                ph,
                rainfall,
                date
            FROM predictions
            WHERE farmer_id = ?
            ORDER BY id DESC
            LIMIT 1
            """,
            (farmer_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return dict(row)

    finally:
        conn.close()


@app.get("/crop/latest/{farmer_id}")
def latest_crop(farmer_id: int):

    if not farmer_exists(farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    crop = get_crop_recommendation(farmer_id)

    if not crop:
        return {
            "status": "no_data",
            "message": "No ML crop recommendation is available yet."
        }

    return {
        "status": "success",
        "data": crop
    }


# =========================================================
# ML CROP PREDICTION
# =========================================================

@app.post("/crop/predict")
def predict_crop(data: CropPredictionRequest):

    if not farmer_exists(data.farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    try:

        import joblib

        model_path = "models/crop_model.pkl"

        if not os.path.exists(model_path):

            raise HTTPException(
                status_code=500,
                detail="ML model file models/crop_model.pkl was not found."
            )

        model = joblib.load(model_path)

        features = [[
            data.nitrogen,
            data.phosphorus,
            data.potassium,
            data.temperature,
            data.humidity,
            data.ph,
            data.rainfall
        ]]

        prediction = model.predict(features)[0]

        crop = str(prediction)

        conn = get_connection()

        try:

            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO predictions (
                    farmer_id,
                    crop,
                    temperature,
                    humidity,
                    nitrogen,
                    phosphorus,
                    potassium,
                    ph,
                    rainfall,
                    date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    data.farmer_id,
                    crop,
                    data.temperature,
                    data.humidity,
                    data.nitrogen,
                    data.phosphorus,
                    data.potassium,
                    data.ph,
                    data.rainfall,
                    datetime.now().isoformat()
                )
            )

            conn.commit()

        finally:
            conn.close()

        return {
            "status": "success",
            "crop": crop
        }

    except HTTPException:
        raise

    except Exception as e:

        print("ML prediction error:", e)

        raise HTTPException(
            status_code=500,
            detail="Crop prediction failed."
        )



# =========================================================
# AUTOMATIC ML PREDICTION FROM LATEST FARM DATA
# =========================================================

@app.post("/crop/predict-latest/{farmer_id}")
def predict_latest_crop(farmer_id: int):
    """
    Run the existing ML model using the farmer's latest farm reading.

    This is the endpoint the mobile app can call after manual entry or
    after an IoT sensor update. The farmer does not need to enter the
    seven ML values again.
    """
    if not farmer_exists(farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    reading = get_latest_farm_reading(farmer_id)

    if not reading:
        raise HTTPException(
            status_code=404,
            detail="No farm data is available for this farmer."
        )

    required_fields = [
        "nitrogen",
        "phosphorus",
        "potassium",
        "temperature",
        "humidity",
        "ph",
        "rainfall"
    ]

    missing_fields = [
        field
        for field in required_fields
        if reading.get(field) is None
    ]

    if missing_fields:
        raise HTTPException(
            status_code=400,
            detail={
                "message": "Latest farm reading is missing ML values.",
                "missing_fields": missing_fields
            }
        )

    try:
        import joblib

        model_path = "models/crop_model.pkl"

        if not os.path.exists(model_path):
            raise HTTPException(
                status_code=500,
                detail="ML model file models/crop_model.pkl was not found."
            )

        model = joblib.load(model_path)

        features = [[
            reading["nitrogen"],
            reading["phosphorus"],
            reading["potassium"],
            reading["temperature"],
            reading["humidity"],
            reading["ph"],
            reading["rainfall"]
        ]]

        prediction = model.predict(features)[0]
        crop = str(prediction)

        conn = get_connection()

        try:
            cursor = conn.cursor()

            cursor.execute(
                """
                INSERT INTO predictions (
                    farmer_id,
                    crop,
                    temperature,
                    humidity,
                    nitrogen,
                    phosphorus,
                    potassium,
                    ph,
                    rainfall,
                    date
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    farmer_id,
                    crop,
                    reading["temperature"],
                    reading["humidity"],
                    reading["nitrogen"],
                    reading["phosphorus"],
                    reading["potassium"],
                    reading["ph"],
                    reading["rainfall"],
                    datetime.now().isoformat()
                )
            )

            conn.commit()
            prediction_id = cursor.lastrowid

        finally:
            conn.close()

        return {
            "status": "success",
            "prediction_id": prediction_id,
            "crop": crop,
            "reading_id": reading["id"],
            "source": reading["source"],
            "farm_data": reading
        }

    except HTTPException:
        raise

    except Exception as e:
        print("Automatic ML prediction error:", e)

        raise HTTPException(
            status_code=500,
            detail="Automatic crop prediction failed."
        )


# =========================================================
# FARM CONTEXT FOR AI
# =========================================================

def get_farm_context(farmer_id):

    reading = get_latest_farm_reading(farmer_id)

    if not reading:

        return "No farm data has been recorded yet."

    return f"""
Nitrogen: {reading['nitrogen']}
Phosphorus: {reading['phosphorus']}
Potassium: {reading['potassium']}
Soil pH: {reading['ph']}
Temperature: {reading['temperature']} °C
Humidity: {reading['humidity']} %
Rainfall: {reading['rainfall']} mm
Soil Moisture: {reading['soil_moisture']} %
Data source: {reading['source']}
Recorded: {reading['date']}
"""


# =========================================================
# AI TEXT ASSISTANT
# =========================================================

@app.post("/ai/ask")
def ai_ask(data: AIRequest):

    if not farmer_exists(data.farmer_id):
        raise HTTPException(
            status_code=404,
            detail="Farmer not found"
        )

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:

        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is missing."
        )

    if not data.question.strip():

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    farm_data = get_farm_context(data.farmer_id)

    crop_data = get_crop_recommendation(
        data.farmer_id
    )

    crop = (
        crop_data["crop"]
        if crop_data
        else "No crop recommendation available."
    )

    try:

        client = genai.Client(
            api_key=api_key
        )

        prompt = f"""
You are AgriSense AI, a friendly farming assistant
for an Indian farmer.

Speak in:
{data.language}

LATEST FARM DATA:
{farm_data}

LATEST ML CROP RECOMMENDATION:
{crop}

FARMER QUESTION:
{data.question}

Rules:
- Use simple language.
- Use actual farm data when relevant.
- Never invent measurements.
- Never claim a disease without sufficient evidence.
- Give practical farming guidance.
- If information is unavailable, say so clearly.
- Keep the answer reasonably concise.
"""

        candidate_models = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite", "gemini-flash-lite-latest", "gemini-3.8-flash", "gemini-3.7-flash"]
        answer = None
        last_error = None
        for cand in candidate_models:
            if not cand:
                continue
            try:
                response = client.models.generate_content(
                    model=cand,
                    contents=prompt
                )
                answer = response.text
                if answer:
                    break
            except Exception as ce:
                last_error = ce
                try:
                    inter = client.interactions.create(model=cand, input=prompt)
                    answer = getattr(inter, "output_text", None)
                    if answer:
                        break
                except Exception as ie:
                    last_error = ie

        if not answer:
            raise RuntimeError(f"All models failed: {last_error}")

        return {
            "status": "success",
            "answer": answer
        }

    except Exception as e:

        print("AI error:", e)

        raise HTTPException(
            status_code=500,
            detail="AI request failed."
        )


# =========================================================
# GEMINI LIVE VOICE
# =========================================================

async def run_gemini(
    websocket,
    language,
    farmer_id
):
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        try:
            await websocket.send_text("ERROR:GEMINI_API_KEY is not set on the server.")
            await websocket.close(code=1008, reason="API Key Missing")
        except Exception:
            pass
        return

    farm_data = get_farm_context(farmer_id)
    crop = get_crop_recommendation(farmer_id)

    print("🌱 Farm data loaded for farmer:", farmer_id)
    print("🌾 ML crop:", crop)

    client = genai.Client(api_key=api_key)

    config = types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        system_instruction=f"""
You are AgriSense AI.
You are a friendly, professional farming assistant speaking directly with an Indian farmer.

SELECTED FARMER LANGUAGE
------------------------
{language}

LATEST FARM DATA
----------------
{farm_data}

LATEST ML CROP RECOMMENDATION
-----------------------------
{crop}

IMPORTANT RULES
1. Always speak in {language}.
2. Use simple language suitable for farmers.
3. Use the farmer's actual farm data whenever relevant.
4. Keep answers conversational, natural and reasonably short.
5. If farm data is unavailable, clearly say so.
"""
    )

    candidate_models = [MODEL, FALLBACK_LIVE_MODEL, "gemini-3.8-live"]
    session = None

    for candidate in candidate_models:
        try:
            print(f"🔌 Connecting Gemini Live using {candidate}...")
            ctx_mgr = client.aio.live.connect(model=candidate, config=config)
            session = await ctx_mgr.__aenter__()
            print(f"✅ Gemini Live connected successfully using {candidate}!")
            break
        except Exception as conn_err:
            print(f"⚠️ Failed connecting to model {candidate}: {conn_err}")

    if not session:
        print("❌ All Gemini Live model connections failed.")
        try:
            await websocket.send_text("ERROR:Failed to connect to Gemini Live voice service.")
            await websocket.close(code=1011, reason="Gemini Live connect error")
        except Exception:
            pass
        return

    browser_connected = True

    try:
        # =================================================
        # GEMINI → BROWSER
        # =================================================
        async def gemini_to_browser():
            nonlocal browser_connected
            try:
                async for response in session.receive():
                    if not browser_connected:
                        break

                    if not response.server_content:
                        continue

                    content = response.server_content

                    # AI Audio
                    if content.model_turn:
                        for part in content.model_turn.parts:
                            if part.inline_data and part.inline_data.data:
                                try:
                                    await websocket.send_bytes(part.inline_data.data)
                                except (WebSocketDisconnect, RuntimeError):
                                    browser_connected = False
                                    return

                    # AI Text transcription
                    if content.output_transcription:
                        text = content.output_transcription.text
                        if text:
                            try:
                                await websocket.send_text("AI_TEXT:" + text)
                            except (WebSocketDisconnect, RuntimeError):
                                browser_connected = False
                                return

                    # Turn complete
                    if content.turn_complete:
                        try:
                            await websocket.send_text("AI_DONE")
                        except (WebSocketDisconnect, RuntimeError):
                            browser_connected = False
                            return

            except asyncio.CancelledError:
                raise
            except Exception as e:
                print("❌ Gemini receive error:", e)
                browser_connected = False

        # =================================================
        # BROWSER → GEMINI
        # =================================================
        async def browser_to_gemini():
            nonlocal browser_connected
            try:
                while browser_connected:
                    try:
                        message = await websocket.receive()
                    except WebSocketDisconnect:
                        print("🔌 Browser disconnected.")
                        browser_connected = False
                        return
                    except RuntimeError as e:
                        print("🔌 Browser socket closed:", e)
                        browser_connected = False
                        return

                    message_type = message.get("type")
                    if message_type == "websocket.disconnect":
                        print("🔌 Browser sent disconnect frame.")
                        browser_connected = False
                        return

                    # AUDIO FROM FARMER
                    audio = message.get("bytes")
                    if audio:
                        try:
                            await session.send_realtime_input(
                                audio=types.Blob(
                                    data=audio,
                                    mime_type="audio/pcm;rate=16000"
                                )
                            )
                        except Exception as e:
                            print("❌ Gemini audio send error:", e)
                            browser_connected = False
                            return
                        continue

                    # TEXT FROM FARMER
                    text = message.get("text")
                    if text:
                        text = text.strip()
                        if not text:
                            continue
                        print("👨‍🌾 Farmer:", text)
                        try:
                            await session.send_realtime_input(text=text)
                        except Exception as e:
                            print("❌ Gemini text send error:", e)
                            browser_connected = False
                            return

            except asyncio.CancelledError:
                raise
            except Exception as e:
                print("❌ Browser receive error:", e)
                browser_connected = False

        receive_task = asyncio.create_task(gemini_to_browser())
        send_task = asyncio.create_task(browser_to_gemini())

        done, pending = await asyncio.wait(
            [receive_task, send_task],
            return_when=asyncio.FIRST_COMPLETED
        )
        browser_connected = False

        for task in (receive_task, send_task):
            if not task.done():
                task.cancel()

        await asyncio.gather(receive_task, send_task, return_exceptions=True)

    finally:
        try:
            await ctx_mgr.__aexit__(None, None, None)
        except Exception:
            pass

        print("🔌 Gemini Live session ended cleanly.")
        try:
            await websocket.close(code=1000, reason="Session ended")
        except Exception:
            pass


# =========================================================
# LIVE VOICE WEBSOCKET
# =========================================================

@app.websocket("/live")
async def live(websocket: WebSocket):
    print("\n================================")
    print("🔎 /live WebSocket request received")
    print("================================")

    try:
        await websocket.accept()
        print("✅ Browser WebSocket accepted")
    except Exception as e:
        print("❌ WebSocket accept failed:", repr(e))
        return

    language = websocket.query_params.get("language", "English")
    farmer_id_raw = websocket.query_params.get("farmer_id")

    print("🌐 Language:", language)
    print("👨‍🌾 Farmer ID:", farmer_id_raw)

    if not farmer_id_raw:
        try:
            await websocket.send_text("ERROR:Farmer ID is missing.")
            await websocket.close(code=1008, reason="Farmer ID missing")
        except Exception:
            pass
        return

    try:
        farmer_id = int(farmer_id_raw)
    except (TypeError, ValueError):
        try:
            await websocket.send_text("ERROR:Invalid Farmer ID.")
            await websocket.close(code=1008, reason="Invalid Farmer ID")
        except Exception:
            pass
        return

    if not farmer_exists(farmer_id):
        try:
            await websocket.send_text("ERROR:Farmer not found in database.")
            await websocket.close(code=1008, reason="Farmer not found")
        except Exception:
            pass
        return

    print("🌱 Farm data validated for farmer:", farmer_id)

    try:
        await run_gemini(websocket, language, farmer_id)
    except WebSocketDisconnect:
        print("🔌 Farmer disconnected")
    except Exception as e:
        print("❌ Server error in /live:", repr(e))
        try:
            await websocket.send_text(f"ERROR:Voice assistant error: {str(e)}")
            await websocket.close(code=1011, reason="Internal error")
        except Exception:
            pass


if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting AgriSense Live Voice Backend Server on http://0.0.0.0:8000 ...")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
