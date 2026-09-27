# 📡 AgriSense AI — ESP32 Complete Hardware Wiring & Setup Guide

This guide details the exact pin-to-pin wiring for:
1. **7-in-1 Industrial Soil Sensor** (Moisture, Temp, EC, pH, Nitrogen, Phosphorus, Potassium) via **MAX485 Modbus Module**
2. **Raindrop / Rainfall Sensor**
3. **DHT22** (Air Temperature & Air Humidity)
4. **ESP32 DevKit V1**

---

## 🔌 Complete Pin-to-Pin Wiring Diagram

```
                 +--------------------------------------+
                 |               ESP32                  |
                 |                                      |
 DHT22 DATA <--->| GPIO 4                               |
 RAIN SENSOR <---| GPIO 34 (ADC1_CH6)                   |
 MAX485 RO   --->| GPIO 16 (RX2)                        |
 MAX485 DI   <---| GPIO 17 (TX2)                        |
 MAX485 DE+RE<---| GPIO 5                               |
                 |                                      |
         GND <---| GND                                  |
        3.3V <---| 3.3V                                 |
          5V <---| VIN / 5V                             |
                 +--------------------------------------+
```

### Detailed Connections Table:

| Module / Sensor | Module Pin | ESP32 Pin / Power | Wire Color / Function |
|---|---|---|---|
| **DHT22** | **VCC** | `3.3V` | Power (3.3V) |
| | **GND** | `GND` | Ground |
| | **DATA** | **`GPIO 4`** | Digital Data (with 10k pullup to 3.3V) |
|---|---|---|---|
| **Rainfall Sensor** | **VCC** | `3.3V` or `5V` | Power |
| | **GND** | `GND` | Ground |
| | **AO** (Analog Out)| **`GPIO 34`** | Analog Reading (ADC1) |
|---|---|---|---|
| **MAX485 TTL Module** | **VCC** | `5V` (VIN) | Power 5V |
| | **GND** | `GND` | Ground |
| | **RO** (Receiver Out)| **`GPIO 16`** | Connects to ESP32 RX2 |
| | **DI** (Driver In)  | **`GPIO 17`** | Connects to ESP32 TX2 |
| | **DE & RE** (Tied) | **`GPIO 5`** | Direction Control Pin |
| | **A** | 7-in-1 Sensor **A (Yellow/Brown)** | RS485 Differential (+) |
| | **B** | 7-in-1 Sensor **B (Blue/Black)**   | RS485 Differential (-) |
|---|---|---|---|
| **7-in-1 Soil Sensor Power** | **VCC (Brown/Red)**| **External 9V-24V DC (+)** | ⚠️ Sensor requires 9V-24V power |
| | **GND (Black)**| **External DC (-) & ESP32 GND** | Common Ground with ESP32 |

---

## 🛠️ Arduino IDE Setup

1. Open **Arduino IDE**.
2. Go to **Tools ➔ Manage Libraries...** and install:
   - `DHT sensor library` by Adafruit
   - `ArduinoJson` by Benoit Blanchon (version 6 or 7)
3. Open [`esp32/agrisense_esp32.ino`](agrisense_esp32.ino).
4. Update lines 23–27 with your WiFi credentials and your computer's IP address:
   ```cpp
   const char* WIFI_SSID     = "Your_WiFi_Name";
   const char* WIFI_PASSWORD = "Your_WiFi_Password";
   const char* BACKEND_URL   = "http://192.168.1.100:8000/sensor/data";
   ```
5. Select board **ESP32 Dev Module**, choose your COM port, and click **Upload**.
6. Open **Serial Monitor** at **115200 baud** to see live readings!
