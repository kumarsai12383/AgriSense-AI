# 🌱 AgriSense AI - Smart Crop Recommendation & Agricultural Assistant

AgriSense AI is an intelligent agricultural decision-support platform designed to assist farmers with AI-driven crop recommendations, soil health analysis, personalized fertilizer and irrigation guidance, plant disease detection, and multilingual voice interaction.

---

## 🚀 Features

- **🌾 AI Crop Recommendation**: Uses a Random Forest machine learning model trained on soil nutrients (N, P, K, pH) and climate parameters (temperature, humidity, rainfall) to recommend the optimal crop.
- **🧪 Soil Health & NPK Diagnostics**: Analyzes soil nutrient levels, categorizes soil quality, and provides actionable improvement tips.
- **🌿 Fertilizer Advisor**: Calculates nutrient deficiencies and provides crop-specific fertilization schedules for 22 major agricultural crops.
- **💧 Irrigation Advisor**: Monitors soil moisture and environmental metrics to determine watering frequency and irrigation urgency.
- **🦠 Plant Disease Detection**: Upload or capture plant leaf photos to identify plant pathologies and receive organic/chemical treatment advice via Gemini Multimodal Vision.
- **🤖 Multilingual AI Chat & Live Voice**:
  - Conversational AI assistant supporting **English, Telugu (తెలుగు), Hindi (हिंदी), Tamil (தமிழ்), Kannada (ಕನ್ನಡ), and Marathi (मराठी)**.
  - Real-time live audio conversations powered by FastAPI WebSockets and Google Gemini Live API.
- **📁 Persistent Farmer Profiles**: Tracks farm readings and prediction histories in a local SQLite database.

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit (Mobile-first responsive CSS, Multilingual UI)
- **ML / Data**: Scikit-Learn (Random Forest Classifier), Pandas, NumPy, Joblib
- **Generative AI & Vision**: Google GenAI SDK (Gemini 3.7 Flash & Gemini Live Preview)
- **Backend / Real-time Voice**: FastAPI, Uvicorn, WebSockets
- **Database**: SQLite3

---

## 📦 Installation & Setup

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone <repo-url>
cd SmartCropRecommendation

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Linux/macOS
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API Key
Set your Google Gemini API key as an environment variable:
```powershell
# Windows PowerShell
$env:GEMINI_API_KEY="your_actual_gemini_api_key"

# Linux / macOS
export GEMINI_API_KEY="your_actual_gemini_api_key"
```

---

## 🚜 Running the Application

### 1. Start the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

### 2. (Optional) Start the Live Voice WebSocket Server
To enable real-time voice streaming with AgriSense AI:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

---

## 🧠 Model Training

To retrain the crop recommendation model using the dataset:
```bash
python train_model.py
```
The trained model artifact will be saved to `models/crop_model.pkl`.

---

## 📂 Project Structure

```
├── app.py                      # Main Streamlit application entry point
├── server.py                   # FastAPI + WebSocket server for Live Voice
├── train_model.py              # ML model training script
├── requirements.txt            # Project dependencies
├── README.md                   # Project documentation
│
├── modules/                    # Application feature modules
│   ├── login.py                # Farmer authentication & profile creation
│   ├── farmer_home.py          # Multilingual landing dashboard
│   ├── farm_data.py            # Sensor and manual farm data management
│   ├── crop_recommendation.py  # ML crop prediction logic
│   ├── crop_details.py         # 22-crop agronomy database
│   ├── soil_health.py          # Soil fertility scoring & analysis
│   ├── fertilizer_advisor.py   # Crop-specific fertilizer recommendations
│   ├── irrigation_advisor.py   # Moisture-based watering recommendations
│   ├── disease_detection.py    # Gemini Vision leaf disease diagnostics
│   ├── ai_assistant_page.py    # Text-based agronomy chatbot
│   ├── ai_engine.py            # Gemini API integration helper
│   ├── live_voice_page.py      # In-app real-time voice interface
│   ├── live_context.py         # DB context extractor for voice agent
│   └── prediction_history.py   # Past prediction log table & export
│
├── database/                   # SQLite database & data access layer
│   ├── agrisense.db            # SQLite database
│   ├── database.py             # Schema initialization & table migrations
│   ├── farmers.py              # Farmer profile queries
│   ├── prediction_db.py        # Prediction recorder
│   └── read_predictions.py     # History loader
│
├── dataset/                    # Data sources
│   └── Crop_recommendation.csv # 2,200 row agricultural dataset
│
├── models/
│   └── crop_model.pkl          # Trained Random Forest model
│
└── notebook/
    └── crop_prediction.ipynb   # Exploratory data analysis & model experiments
```
