# 📡 AgriSense AI — ESP32 Live IoT Sensor Integration Guide

This guide explains how to connect your ESP32 board with soil and weather sensors to stream live farm telemetry directly into **AgriSense AI**.

---

## 🛠️ Hardware Requirements

| Component | Function | Interface / Pin |
|---|---|---|
| **ESP32 NodeMCU / DevKit V1** | Main Microcontroller & WiFi Gateway | USB / 3.3V |
| **DHT22 / DHT11** | Temperature & Air Humidity | GPIO 4 |
| **Capacitive Soil Moisture v1.2** | Real-time Soil Moisture % | Analog GPIO 34 (ADC1_CH6) |
| **Soil pH Sensor Probe** | Soil Acidity / Alkalinity (pH) | Analog GPIO 35 (ADC1_CH7) |
| **MAX485 Module + NPK Sensor** *(Optional)* | Nitrogen, Phosphorus, Potassium | Hardware Serial2 (GPIO 16/17, DE/RE GPIO 5) |

---

## 🔌 Pin Connections & Wiring Diagram

### 1. DHT22 / DHT11 Temperature & Humidity Sensor
- **VCC** ➔ ESP32 `3.3V` or `5V`
- **GND** ➔ ESP32 `GND`
- **DATA** ➔ ESP32 `GPIO 4` *(with 10k pull-up resistor to 3.3V if standalone)*

### 2. Capacitive Soil Moisture Sensor v1.2
- **VCC** ➔ ESP32 `3.3V`
- **GND** ➔ ESP32 `GND`
- **AOUT** ➔ ESP32 `GPIO 34`

### 3. Soil pH Sensor Probe
- **VCC** ➔ ESP32 `5V`
- **GND** ➔ ESP32 `GND`
- **AOUT / PO** ➔ ESP32 `GPIO 35`

### 4. MAX485 TTL to RS485 Module (for NPK Sensor)
- **VCC** ➔ ESP32 `5V`
- **GND** ➔ ESP32 `GND`
- **RO (Receiver Out)** ➔ ESP32 `GPIO 16` (RX2)
- **DI (Driver In)** ➔ ESP32 `GPIO 17` (TX2)
- **DE & RE (Jumpered together)** ➔ ESP32 `GPIO 5`
- **A** ➔ RS485 NPK Sensor Brown/A line
- **B** ➔ RS485 NPK Sensor Black/B line

---

## 💻 Arduino IDE Setup Instructions

### 1. Install Required Arduino Libraries
Open **Arduino IDE** ➔ Go to **Tools** ➔ **Manage Libraries...** and install:
1. `DHT sensor library` by Adafruit
2. `Adafruit Unified Sensor`
3. `ArduinoJson` (v6.x or v7.x) by Benoit Blanchon

### 2. Configure Your Settings in `agrisense_esp32.ino`
Edit lines 23–30 with your WiFi details and server URL:
```cpp
const char* WIFI_SSID     = "Your_WiFi_Name";
const char* WIFI_PASSWORD = "Your_WiFi_Password";
const char* BACKEND_URL   = "http://192.168.1.100:8000/sensor/data"; // Replace with your server IP
const int FARMER_ID       = 1;
```

> **How to find your local PC IP address:**
> In Windows PowerShell, run: `ipconfig` (Look for *IPv4 Address*, e.g., `192.168.1.xxx`).

### 3. Upload Code to ESP32
1. Connect ESP32 via USB cable.
2. Select Board: **ESP32 Dev Module**.
3. Select the correct **COM Port**.
4. Click **Upload** (Hold `BOOT` button on ESP32 if upload stays on "Connecting...").
5. Open **Serial Monitor** at **115200 baud rate** to view live sensor telemetry!
