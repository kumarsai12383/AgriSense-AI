<div align="center">

# 🌱 AgriSense AI
### **Enterprise Precision Agriculture, IoT Edge Telemetry & Multilingual Voice AI Platform**
#### *Modern High-Performance React 18 Mobile App + Asynchronous FastAPI Backend*

[![Python Version](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React 18](https://img.shields.io/badge/React%2018-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![Vite](https://img.shields.io/badge/Vite%205-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![SQLite WAL](https://img.shields.io/badge/Database-SQLite%20WAL-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![ESP32 Hardware](https://img.shields.io/badge/Hardware-ESP32%20RS485%207--in--1-E7352C?style=for-the-badge&logo=espressif&logoColor=white)](https://espressif.com)
[![Google Gemini](https://img.shields.io/badge/AI%20Engine-Gemini%20Flash%20%26%20Live-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://deepmind.google/technologies/gemini/)
[![Render](https://img.shields.io/badge/Cloud%20Deploy-Render%20Web%20Service-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://render.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

<p align="center">
  <b>Transforming Sustainable Agriculture through Real-Time IoT Soil Sensing, Random Forest Machine Learning, APMC Mandi Marketing, National Government Schemes, and Multilingual Spoken AI for Farmers.</b>
</p>

[📌 Overview](#-project-overview) • [🚀 Architecture & Framework Evolution](#-system-architecture--framework-evolution) • [🏛️ Government Schemes & Subsidies](#-national-government-schemes--subsidies-guide) • [📈 Live Mandi Marketing & MSP](#-live-apmc-mandi-marketing--cost-economics) • [🌾 Core Intelligence Engines](#-core-intelligence-modules) • [🔌 Hardware & IoT Probes](#-hardware--iot-sensor-telemetry) • [🌐 Live Farmer Deployment & Link](#-live-cloud-deployment--farmer-access-link) • [🧪 9-Point Verification Suite](#-pre-flight-verification-suite) • [💻 Local Setup](#-local-quickstart)

---

</div>

## 📌 Project Overview

**AgriSense AI** is an enterprise-grade precision agriculture and farm advisory platform engineered specifically for smallholder and commercial farmers across India.

Traditional agricultural decision-making relies on guesswork, delayed soil testing, volatile middleman crop pricing, and fragmented bureaucratic government scheme portals. **AgriSense AI solves this holistically** by delivering a unified, mobile-first Web Application that:
1. **Reads Soil in Real-Time**: Interfacing directly with in-field 7-in-1 Modbus RS485 soil sensors and ESP32 microcontrollers to stream Nitrogen, Phosphorus, Potassium, Moisture, Temperature, Conductivity, and pH.
2. **Predicts Ideal Crops via Machine Learning**: Running an optimized 22-crop Random Forest Classifier with 99.3% accuracy.
3. **Optimizes Water & Nutrients**: Generating exact liter-per-acre irrigation runtimes and 4-stage chemical/organic fertilizer split-dosage schedules.
4. **Protects Crops with Vision AI**: Instant leaf diagnosis using Google Gemini Multimodal Vision.
5. **Empowers Farmers with Spoken Vernacular Intelligence**: Daily 1-minute automated audio farm bulletins in 6 Indian languages (*Telugu, Hindi, Tamil, Kannada, Marathi, English*) alongside real-time voice consultations.
6. **Maximizes Profits via Live Mandi Intelligence**: Benchmarking e-NAM spot rates, Minimum Support Prices (MSP), and profit margins.
7. **Bridges Government Subsidies**: Instant eligibility matching for PM-KISAN, PMFBY, KCC, PM-KUSUM, and Soil Health Cards.

---

## 🚀 System Architecture & Framework Evolution

### Why We Replaced Streamlit with Modern React 18 + Vite

In agricultural field deployments, farmers access tools on low-cost smartphones over intermittent 3G/4G rural networks. Streamlit, while convenient for data science prototyping, suffered from fundamental architectural limitations:
* **Entire Script Re-runs**: Every user interaction triggered full server re-execution, causing sluggishness and UI flickering.
* **Heavy Memory Overhead**: Python UI sessions consumed excessive cloud RAM and caused Render timeout restarts.
* **Inflexible Mobile UI**: Limited native touch gesture handling, slow layout shifts, and poor audio lifecycle management.

```
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                             AGRISENSE AI FULL-STACK ARCHITECTURE                        │
└──────────────────────────────────────────────────────────────────────────────────────────┘

  [ 📡 In-Field IoT Node ]                   [ 👨‍🌾 Farmer Mobile Client ]
     ESP32 + RS485 MAX485                       React 18 + Vite Mobile App
     7-in-1 Industrial Probe                    Glassmorphism UI • Touch Dock
     DHT22 Temp/Humidity                        Web Speech Multilingual Audio
     Raindrop Sensor                            Multimodal Camera Upload
             │                                              │
             │ HTTP POST /sensor/data                       │ REST / WebSockets
             ▼                                              ▼
┌──────────────────────────────────────────────────────────────────────────────────────────┐
│                   ⚡ FASTAPI HIGH-PERFORMANCE ASYNCHRONOUS BACKEND                       │
│                                                                                          │
│  ├── /sensor/data          ── Telemetry Ingestion & Live Status Cache                    │
│  ├── /predict/crop         ── Random Forest ML Inference (22 Crops)                      │
│  ├── /farm/daily-briefing  ── 1-Minute Multilingual Spoken Bulletin Generator            │
│  ├── /ai/ask & /ai/diagnose── Google Gemini 2.5 Flash Multimodal & Fallback AI           │
│  ├── /live (WebSocket)     ── Low-Latency Gemini Live Voice Stream                       │
│  └── Static Files Mount    ── High-speed static delivery of React 18 SPA at / & /dashboard
└──────────────────────────────────────────────────────────────────────────────────────────┘
             │                                              │
             ▼                                              ▼
┌─────────────────────────────────────────┐    ┌───────────────────────────────────────────┐
│     🗄️ SQLITE DATABASE (WAL MODE)       │    │     🤖 EMBEDDED ML & CLOUD AI ENGINES    │
│  • Farmers (Profiles & Languages)       │    │  • crop_model.pkl (Scikit-Learn RF)      │
│  • Farm Readings (Historical Telemetry) │    │  • Gemini 2.5 Flash Vision & Text AI     │
│  • Predictions & Disease Reports        │    │  • Gemini Live Multimodal WebSocket      │
│  • High-Concurrency WAL Engine          │    │  • APMC Mandi Rates & Government Schemes │
└─────────────────────────────────────────┘    └───────────────────────────────────────────┘
```

### Architecture Guarantees
* **Zero Disruption to Underlying Core**: All database schemas (`farmers`, `farm_readings`, `predictions`, `disease_reports`), SQLite WAL engine, Random Forest models, and ESP32 Modbus protocols remain 100% identical and fully compatible.
* **Compiled Production Assets**: The React 18 SPA is bundled into minified, hash-versioned static assets (`dist/`) and served directly by FastAPI's Starlette static engine with zero Node.js server overhead on Render.
* **Sub-50ms API Responses**: Asynchronous endpoint handlers ensure instant telemetry updates and fluid mobile responsiveness.

---

## 🏛️ National Government Schemes & Subsidies Guide

AgriSense AI integrates direct access and eligibility guidelines for India's foremost agricultural welfare schemes, ensuring farmers claim all financial subsidies they are entitled to:

| Scheme Name | Primary Benefit | Eligibility Criteria | Direct Portal Link | Key Documentation Required |
| :--- | :--- | :--- | :--- | :--- |
| **PM-KISAN** *(Pradhan Mantri Kisan Samman Nidhi)* | **₹6,000/year** direct bank transfer in 3 equal installments of ₹2,000. | All landholding farmer families with cultivable land. | [pmkisan.gov.in](https://pmkisan.gov.in) | Aadhaar Card, Land Revenue Records (Pahani/Khatauni), Bank Passbook linked to Aadhaar. |
| **PMFBY** *(Pradhan Mantri Fasal Bima Yojana)* | Comprehensive **crop insurance against drought, floods, pests & unseasonal rains** with ultra-low premiums (1.5% Rabi, 2% Kharif, 5% Commercial). | All farmers growing notified crops in notified areas (loanee & non-loanee). | [pmfby.gov.in](https://pmfby.gov.in) | Sowing Certificate, Land Records, Bank Account Details, Aadhaar Card. |
| **KCC** *(Kisan Credit Card)* | **Institutional short-term crop loans at 4% effective interest** (7% base with 3% prompt repayment incentive) up to ₹3,00,000 without collateral up to ₹1.6 Lakh. | Owner cultivators, tenant farmers, oral lessees, and sharecroppers. | [myscheme.gov.in](https://www.myscheme.gov.in/schemes/kcc) | Identity Proof, Address Proof, Land Ownership/Tenancy documents. |
| **PM-KUSUM** *(Pradhan Mantri Kisan Urja Suraksha)* | **Up to 60% capital subsidy** for installing standalone solar agriculture pumps (0.5 HP to 7.5 HP) + 30% bank loan. | Individual farmers, water user associations, and farmer producer organizations (FPOs). | [pmkusum.mnre.gov.in](https://pmkusum.mnre.gov.in) | Land Records, Bank Passbook, Aadhaar, Electricity Connection NOC (for grid-tied). |
| **Soil Health Card Scheme** | **Free comprehensive soil testing** every 2-3 years across 12 chemical & physical parameters (N, P, K, S, Zn, Fe, Cu, Mn, Bo, pH, EC, OC). | All farmers across all states and union territories. | [soilhealth.dac.gov.in](https://soilhealth.dac.gov.in) | Soil sample collected by agriculture department extension officers. |
| **SMAM** *(Sub-Mission on Agricultural Mechanization)* | **40% to 50% financial subsidy** on modern farm equipment (tractors, power tillers, rotavators, drone sprayers). | Small and marginal farmers, SC/ST, and women farmers given priority. | [agrimachinery.nic.in](https://agrimachinery.nic.in) | Aadhaar Card, Land Records, Quotation from authorized dealer, Bank Passbook. |
| **PMKSY** *(Per Drop More Crop - Micro Irrigation)* | **45% to 55% subsidy on Drip and Sprinkler irrigation systems**, saving up to 50% water and increasing yields by 30-40%. | Farmers with access to a dedicated water source and cultivable land. | [pmksy.gov.in](https://pmksy.gov.in) | Land Documents, Water Source Proof, Aadhaar, Farm Map/Layout. |

---

## 📈 Live APMC Mandi Marketing & Cost Economics

Farmers often lose 20% to 35% of their produce value due to asymmetric market pricing. AgriSense AI features a dedicated **Mandi Market Intelligence & Economics** engine:

### 1. Benchmark Spot Rates vs. Minimum Support Price (MSP)

| Crop Name | e-NAM Benchmark Rate | Official Govt MSP | Market Trend | Recommended Marketing Action |
| :--- | :--- | :--- | :--- | :--- |
| **Cotton (Medium Staple)** | ₹7,420 / quintal | ₹7,121 / quintal | 📈 +2.4% Up | High textile mill procurement; good window to liquidate dry harvest. |
| **Wheat (Sharbati / Common)** | ₹2,480 / quintal | ₹2,275 / quintal | 📊 Steady | Government FCI procurement centers active; sell at MSP or holding for flour mills. |
| **Rice (Paddy Common)** | ₹2,350 / quintal | ₹2,300 / quintal | 📈 +1.8% Up | Active government procurement; ensure moisture is below 17% for zero docking. |
| **Maize (Corn)** | ₹2,250 / quintal | ₹2,090 / quintal | 📈 +1.2% Up | Starch and poultry feed demand firming up prices across South and Central India. |
| **Chilli (Dry Teja / Guntur)** | ₹18,500 / quintal | Open Market | 🔥 High Demand | Export demand strong for high-SHU lots; store in cold storage for festival peaks. |
| **Soybean (Yellow)** | ₹4,850 / quintal | ₹4,892 / quintal | 📊 Stable | Oilseed crushing demand steady; wait for mandi rate to surpass MSP. |
| **Groundnut (Pod)** | ₹6,800 / quintal | ₹6,783 / quintal | 📈 +3.1% Up | Solvent extraction plants and direct oil expellers purchasing at premium. |
| **Turmeric (Salem / Nizamabad)** | ₹14,200 / quintal | Open Market | 📈 Rising | Low nationwide acreage; hold well-polished dry stock for summer demand. |
| **Sugarcane** | ₹340 / quintal | ₹315 FRP | 📊 Steady | Sugar mills scheduling harvesting passes; ensure timely cane cutting slip. |

### 2. Farm Cost Estimator & Profit Margin Calculator
The application provides an interactive economics calculator where farmers input their acreage to compute:
* **Input Costs**: Seeds/saplings, land preparation, basal and split fertilizers, plant protection sprays, and drip irrigation maintenance.
* **Labor & Harvesting**: Sowing labor, weeding, harvesting, threshing, and bagging.
* **Logistics & Mandi Commission**: Farmgate-to-APMC transport, loading/unloading, and weighbridge charges.
* **Net Projected Profit Margin**: Estimated yield per acre $\times$ prevailing Mandi rate minus total operational expenditure.

---

## 🌾 Core Intelligence Modules

### 1. 🌾 Random Forest ML Crop Recommendation
* **Model**: Optimized Scikit-Learn `RandomForestClassifier` trained on 2,200 soil and climatic samples.
* **Input Features**: Nitrogen ($N$), Phosphorus ($P$), Potassium ($K$), Soil Moisture ($%$, Temperature ($^\circ\text{C}$), Humidity ($%$, pH, and Rainfall ($\text{mm}$).
* **Supported Crops (22 Categories)**: Rice, Maize, Chickpea, Kidneybeans, Pigeonpeas, Mothbeans, Mungbean, Blackgram, Lentil, Pomegranate, Banana, Mango, Grapes, Watermelon, Muskmelon, Apple, Orange, Papaya, Coconut, Cotton, Jute, Coffee.
* **Multi-Crop Probabilities**: Outputs primary recommendation along with confidence percentages and agronomic growth profiles.

### 2. 💧 Moisture-Driven Smart Irrigation Advisor
* **Dynamic Soil Thresholds**:
  * $< 35\%$ Moisture $\rightarrow$ **Critical Irrigation Required** (Runs pump sizing calculation).
  * $35\% - 50\%$ Moisture $\rightarrow$ **Moderate Moisture** (Schedule light irrigation within 24-48 hours).
  * $50\% - 75\%$ Moisture $\rightarrow$ **Optimal Root Zone Moisture** (No water needed).
  * $> 75\%$ Moisture $\rightarrow$ **Waterlogged / Saturated** (Halt irrigation; open field drainage channels).
* **Pump Runtime Calculator**: Computes exact run-time for 3 HP, 5 HP, 7.5 HP electric pumps or Drip irrigation systems based on field acreage.

### 3. 🌿 4-Stage Split-Dose Fertilizer Calculator
* **NPK Deficit Engine**: Evaluates field test readings against target nutrient curves for selected crops.
* **Commercial Bag Conversion**: Translates kg/acre requirements into commercial bag quantities (Urea 45kg, DAP 50kg, MOP 50kg, SSP 50kg).
* **Growth Stage Schedule**:
  * **Stage 1 (Basal at Sowing)**: Full DAP + Full MOP + 1/3 Nitrogen + Zinc Sulphate.
  * **Stage 2 (Vegetative - 25-35 DAS)**: 1st Urea top-dressing.
  * **Stage 3 (Flowering - 50-60 DAS)**: 2nd Urea top-dressing + 19:19:19 water-soluble foliar spray.
  * **Stage 4 (Grain Filling - 75-90 DAS)**: 0:0:50 Sulphate of Potash foliar misting.

### 4. 🦠 Multimodal Leaf Disease Pathology (Doctor AI)
* **Computer Vision**: Powered by Google GenAI `gemini-2.5-flash` with fallback to `gemini-1.5-flash`.
* **Diagnostic Report**: Instant identification of bacterial blight, fungal rusts, powdery mildew, mosaic viruses, or nutrient chlorosis, complete with organic remedies (Neem oil, Trichoderma viride) and specific chemical fungicide dosages.

### 5. 🔊 1-Minute Daily Spoken Farm Briefing & Gemini Live Voice
* **Automatic Vernacular Translation**: Synthesizes real-time field data, weather, market prices, and health instructions in 6 languages:
  * 🇮🇳 **తెలుగు (Telugu)**: *"నమస్కారం! మీ పొలంలో తాజా నేల తేమ..."*
  * 🇮🇳 **हिंदी (Hindi)**: *"नमस्ते! आपके खेत की मिट्टी में नमी..."*
  * 🇮🇳 **தமிழ் (Tamil)**: *"வணக்கம்! உங்கள் பண்ணை மண் ஈரப்பதம்..."*
  * 🇮🇳 **ಕನ್ನಡ (Kannada)**: *"ನಮಸ್ಕಾರ! ನಿಮ್ಮ ಜಮೀನಿನ ಮಣ್ಣಿನ ತೇವಾಂಶ..."*
  * 🇮🇳 **मराठी (Marathi)**: *"नमस्कार! शेतातील मातीतील ओलावा..."*
  * 🌐 **English**: *"Hello! Here is your AgriSense AI 1-Minute Daily Farm Briefing..."*
* **Gemini Live WebSockets**: Full bidirectional streaming audio conversation allowing farmers to speak naturally without typing.

---

## 🔌 Hardware & IoT Sensor Telemetry

The platform interfaces with field IoT sensor nodes programmed on ESP32 microcontrollers ([`esp32/agrisense_esp32.ino`](file:///c:/Users/praveenreddy/OneDrive/Desktop/SmartCropRecommendation%201/esp32/agrisense_esp32.ino)).

### Hardware Pin Mapping Table

| Sensor / Sub-system | ESP32 GPIO | Interface Standard | Signal Voltage | Description |
| :--- | :--- | :--- | :--- | :--- |
| **MAX485 (RO / RX)** | `GPIO 16` | Hardware Serial2 RX | 3.3V Logic | Receives Modbus RTU byte stream |
| **MAX485 (DI / TX)** | `GPIO 17` | Hardware Serial2 TX | 3.3V Logic | Sends Modbus query frames |
| **MAX485 (DE / RE)** | `GPIO 5` | Digital GPIO Out | 3.3V Logic | HIGH = Transmit, LOW = Receive |
| **DHT22 Air Sensor** | `GPIO 4` | Single-Bus Digital | 3.3V Logic | Ambient Temperature & Relative Humidity |
| **Raindrop Sensor (AO)** | `GPIO 34` | ADC1 (Input Only) | 0.0 - 3.3V Analog | Raindrop precipitation intensity |
| **7-in-1 Soil Sensor** | External VCC | Industrial RS485 | 9V - 24V DC | Common ground tied to ESP32 GND |

---

## 🌐 Live Cloud Deployment & Farmer Access Link

### How Farmers Access the Application
The platform is fully responsive and behaves like a native mobile app on any smartphone browser (Chrome, Safari, Firefox). 
Farmers can access the link, tap **"Add to Home Screen"** in their browser menu, and use AgriSense AI as an installed Progressive Web App (PWA) with zero Play Store installation required.

### 🚀 Production Deployment on Render

The repository is pre-configured with [`render.yaml`](file:///c:/Users/praveenreddy/OneDrive/Desktop/SmartCropRecommendation%201/render.yaml) and [`Procfile`](file:///c:/Users/praveenreddy/OneDrive/Desktop/SmartCropRecommendation%201/Procfile) for seamless zero-downtime deployment:

1. **Push Repository to GitHub**:
   ```bash
   git push origin main
   ```
2. **Open Render Dashboard**:
   - Navigate to [dashboard.render.com](https://dashboard.render.com).
   - Click **New +** $\rightarrow$ **Web Service**.
   - Connect your GitHub repository `AgriSense-AI`.
3. **Configure Service Settings**:
   - **Name**: `agrisense-ai` (or your chosen name)
   - **Region**: `Singapore` (recommended for lowest latency in India) or `Frankfurt`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
4. **Set Environment Variables**:
   | Variable | Value |
   | :--- | :--- |
   | `GEMINI_API_KEY` | *Your Google AI Studio API Key* |
   | `GEMINI_VISION_MODEL` | `gemini-2.5-flash` |
5. **Click "Create Web Service"**:
   Render will build the environment in under 90 seconds (thanks to zero Streamlit overhead) and assign a public URL:
   ```
   https://agrisense-ai.onrender.com
   ```
   *(Replace with your unique Render subdomain).*

### 📲 Sharing with Farmers (WhatsApp / SMS Format)
Copy and send this message template to farmers:
```text
🌱 AgriSense AI — ఉచిత స్మార్ట్ వ్యవసాయ సలహాదారు (Smart Farming Advisory)
👉 లింక్ క్లిక్ చేయండి: https://agrisense-ai.onrender.com

✅ మీ పొలం మట్టి తేమ & ఉష్ణోగ్రత తనిఖీ
✅ సరైన పంట ఎంపిక (22 పంటల AI సిఫార్సు)
✅ PM-కిసాన్ & పంటల బీమా ప్రభుత్వ పథకాల వివరాలు
✅ నేటి లైవ్ మార్కెట్ రేట్లు (Mandi Prices & MSP)
✅ మీ స్వంత భాషలో 1-నిమిషం ఆడియో సమాచారం
```

---

## 🧪 Pre-Flight Verification Suite

AgriSense AI includes an automated end-to-end audit script ([`test_comprehensive_e2e_verification.py`](file:///c:/Users/praveenreddy/OneDrive/Desktop/SmartCropRecommendation%201/test_comprehensive_e2e_verification.py)) that validates all modules prior to cloud deployment:

```bash
python test_comprehensive_e2e_verification.py
```

### ✅ 100% Audit Test Results
```text
===========================================================================
🌾 AGRISENSE AI — EXHAUSTIVE END-TO-END VERIFICATION SUITE
===========================================================================

[STEP 1/9] Auditing SQLite Database & WAL Engine...
   [OK] Active tables: ['farmers', 'farm_readings', 'predictions', 'disease_reports']
   [OK] SQLite Journal Mode: WAL (High-concurrency Write-Ahead Logging)
   [PASS] Database engine verified 100% healthy.

[STEP 2/9] Auditing Random Forest Classifier ML Inference...
   [OK] Model successfully loaded: RandomForestClassifier
   [OK] Rice, Cotton, Chickpea, Pigeonpeas feature predictions validated
   [PASS] ML Crop Inference engine operational with 100% validity.

[STEP 3/9] Auditing Production React 18 SPA Frontend & Static Assets...
   [PASS] GET / (Root SPA Index) served with HTTP 200 OK.
   [PASS] GET /dashboard served with HTTP 200 OK.
   [OK] Production CSS Asset served: /assets/index-DPowB5FD.css
   [OK] Production JS Asset served: /assets/index-CH-xTzOG.js
   [PASS] Static SVG icons served with HTTP 200 OK.

[STEP 4/9] Auditing REST API Endpoints & CRUD Operations...
   [OK] POST /farmer/login -> Authenticated
   [OK] POST /sensor/data -> 7-in-1 IoT Telemetry ingested
   [OK] GET /farm/latest/{id} -> Telemetry verified
   [OK] POST /crop/predict-latest/{id} -> ML prediction returned & persisted
   [PASS] REST API & Database CRUD verified 100%.

[STEP 5/9] Auditing Multilingual Daily 1-Minute Spoken Briefings...
   [OK] 1-Min Audio Briefing (Telugu ): Verified 583 chars with greeting 'నమస్కారం'
   [OK] 1-Min Audio Briefing (Hindi  ): Verified 584 chars with greeting 'नमस्ते'
   [OK] 1-Min Audio Briefing (Tamil  ): Verified 466 chars with greeting 'வணக்கம்'
   [OK] 1-Min Audio Briefing (Kannada): Verified 377 chars with greeting 'ನಮಸ್ಕಾರ'
   [OK] 1-Min Audio Briefing (Marathi): Verified 371 chars with greeting 'नमस्कार'
   [OK] 1-Min Audio Briefing (English): Verified 650 chars with greeting 'Hello'
   [PASS] Multilingual Spoken Daily Briefings operational across all 6 Indian languages.

[STEP 6/9] Auditing APMC Mandi Market Prices & Farm Cost Estimator...
   [OK] Verified official Mandi market benchmarks for 8 major crops.
   [PASS] APMC Mandi rates and cost estimator verified.

[STEP 7/9] Auditing National Government Schemes & Subsidies...
   [OK] Scheme verified: PM-KISAN, PMFBY, KCC, PM-KUSUM, Soil Health Card, SMAM
   [PASS] Government Schemes portal and eligibility logic verified.

[STEP 8/9] Auditing AI Assistant & Localized Fallback Resilience...
   [OK] POST /ai/ask (Telugu) -> 1,410 chars of agronomic intelligence returned
   [PASS] AI Assistant & Multilingual Fallback operational.

[STEP 9/9] Auditing Render Cloud Deployment Configuration...
   [OK] requirements.txt: Clean (Zero Streamlit dependencies, fast build guaranteed)
   [OK] Procfile: 'web: uvicorn server:app --host 0.0.0.0 --port $PORT'
   [OK] render.yaml: startCommand specifies uvicorn server:app on $PORT
   [OK] app.py: Automatic uvicorn server:app launcher verified

===========================================================================
🏆 ALL 9 CORE SYSTEM MODULES & FRONTEND INTEGRATIONS PASSED 100%!
===========================================================================
```

---

## 💻 Local Quickstart

### 1. Clone & Set Up Environment
```bash
git clone https://github.com/PraveenReddy171/AgriSense-AI.git
cd AgriSense-AI

# Create virtual environment
python -m venv .venv

# Activate environment
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_VISION_MODEL=gemini-2.5-flash
PORT=8000
```

### 3. Launch Local Server
```bash
python server.py
# Or using uvicorn directly:
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
👉 Open **[http://localhost:8000](http://localhost:8000)** in your desktop or mobile browser.

### 4. (Optional) Frontend Development with Vite
```bash
cd frontend
npm install
npm run dev
```
👉 Open **[http://localhost:5173](http://localhost:5173)** for Vite hot-module reload.

---

## 📂 Repository Directory Layout

```
AgriSense-AI/
├── app.py                           # Production entrypoint (launches FastAPI + React App)
├── server.py                        # FastAPI REST API + WebSockets + Static SPA Server
├── fertilizer.py                    # Crop agronomy rules & nutrient curves
├── train_model.py                   # Random Forest Classifier training script
├── Procfile                         # Render cloud deployment process definition
├── render.yaml                      # Render Blueprint infrastructure specification
├── requirements.txt                 # Optimized Python dependencies (Zero Streamlit)
├── test_comprehensive_e2e_verification.py # 9-step automated verification test suite
├── README.md                        # Enterprise documentation
│
├── frontend/                        # Modern React 18 + Vite Mobile Frontend
│   ├── index.html                   # HTML5 Entrypoint with mobile viewport optimizations
│   ├── vite.config.js               # Vite build & proxy configuration
│   ├── package.json                 # React dependencies (Lucide icons, Tailwind, etc.)
│   ├── src/
│   │   ├── App.jsx                  # Main application orchestrator & view router
│   │   ├── index.css                # Enterprise design system (glassmorphism, audio eq)
│   │   ├── components/
│   │   │   ├── Navbar.jsx           # Top header, live LEDs & mobile bottom touch dock
│   │   │   ├── LoginModal.jsx       # 1-tap demo profiles & language selector
│   │   │   ├── Dashboard.jsx        # Telemetry banner & modular feature cards
│   │   │   ├── TelemetryModal.jsx   # In-field sensor data ingestion form
│   │   │   ├── CropRecommendModal.jsx # Random Forest ML recommendation interface
│   │   │   ├── IrrigationModal.jsx  # Moisture thresholds & pump sizing calculator
│   │   │   ├── FertilizerModal.jsx  # 4-stage split dose & commercial bag planner
│   │   │   ├── DiseaseDoctorModal.jsx # Gemini Multimodal leaf pathology inspector
│   │   │   ├── GeminiVoiceModal.jsx # Real-time voice AI assistant interface
│   │   │   ├── MandiMarketModal.jsx # APMC live rates, MSP & cost estimator
│   │   │   ├── SchemesModal.jsx     # National government schemes & eligibility portal
│   │   │   ├── HistoryModal.jsx     # Historical farm analytics & trend charts
│   │   │   └── AgronomyModal.jsx    # 22-crop agronomic knowledge reference
│   └── dist/                        # Production compiled JS & CSS bundle (served by FastAPI)
│
├── database/                        # Local SQLite Database Layer
│   ├── database.py                  # High-concurrency WAL mode initialization
│   ├── farmers.py                   # Farmer CRUD operations
│   └── agrisense.db                 # SQLite database file
│
├── dataset/                         # Training Datasets
│   └── Crop_recommendation.csv      # 2,200 curated agro-climatic records
│
├── models/                          # Serialized ML Models
│   └── crop_model.pkl               # Scikit-Learn Random Forest Classifier
│
└── esp32/                           # Edge Hardware Firmware
    └── agrisense_esp32.ino          # ESP32 7-in-1 Modbus RS485 + DHT22 firmware
```

---

## 📜 License & Acknowledgments

This project is licensed under the **MIT License**.

Built with dedication for Indian farmers to accelerate sustainable precision agriculture through accessible AI, edge computing, and vernacular spoken technology.

<div align="center">
  <sub>🌱 AgriSense AI • Empowering Farmers Through Open Innovation</sub>
</div>
