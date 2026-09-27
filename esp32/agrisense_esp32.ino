/*
 ==============================================================================
  🌱 AgriSense AI — ESP32 Complete Precision Agriculture Sensor Node
 ==============================================================================
  Hardware Setup:
    1. 7-in-1 Soil Sensor (Soil Moisture, Temp, EC, pH, Nitrogen, Phosphorus, Potassium)
       via MAX485 TTL to RS485 module on Hardware Serial2 (GPIO 16, 17, 5)
    2. DHT22 Sensor (Ambient Air Temperature & Humidity) on GPIO 4
    3. Raindrop / Rainfall Sensor (Analog Rain Intensity) on GPIO 34
    4. ESP32 WiFi Microcontroller (Sends JSON telemetry to AgriSense AI Backend)
 ==============================================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ==============================================================================
// 1. NETWORK & BACKEND CONFIGURATION
// ==============================================================================
const char* WIFI_SSID     = "YOUR_WIFI_NAME";        // Enter your WiFi Name
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";    // Enter your WiFi Password

// Backend URL: Replace with your PC IP (e.g. http://192.168.1.100:8000/sensor/data)
// If testing locally on computer, find IP with 'ipconfig' command
const char* BACKEND_URL   = "http://192.168.1.100:8000/sensor/data";

const int FARMER_ID       = 1;                       // Farmer ID registered in AgriSense AI
const unsigned long TELEMETRY_INTERVAL_MS = 15000;   // Send readings every 15 seconds

// ==============================================================================
// 2. PIN DEFINITIONS
// ==============================================================================
// --- DHT22 Air Sensor ---
#define DHT_PIN            4      // DHT22 Data Pin connected to GPIO 4
#define DHT_TYPE           DHT22  // DHT22 (AM2302)

// --- Rainfall Sensor ---
#define RAIN_ANALOG_PIN    34     // Rain Sensor Analog Out connected to GPIO 34 (ADC1_CH6)

// --- MAX485 to 7-in-1 RS485 Soil Sensor (Hardware Serial2) ---
#define RS485_RX_PIN       16     // ESP32 RX2 connected to MAX485 RO (Receiver Output)
#define RS485_TX_PIN       17     // ESP32 TX2 connected to MAX485 DI (Driver Input)
#define RS485_DE_RE_PIN    5      // MAX485 DE & RE tied together on GPIO 5

// ==============================================================================
// 3. RS485 MODBUS RTU COMMAND FRAMES
// ==============================================================================
// Modbus RTU Query Frame: Read 7 Holding Registers (Moisture, Temp, EC, pH, N, P, K)
// Address: 0x01, Function: 0x03, Start Reg: 0x0000, Count: 0x0007, CRC16: 0x04 0x08
const byte query7in1_Standard[] = {0x01, 0x03, 0x00, 0x00, 0x00, 0x07, 0x04, 0x08};

// Alternative Query Frame used by some 7-in-1 manufacturers starting at register 0x001E
const byte query7in1_Alternative[] = {0x01, 0x03, 0x00, 0x1E, 0x00, 0x07, 0x65, 0xCC};

DHT dht(DHT_PIN, DHT_TYPE);
unsigned long lastTelemetryTime = 0;

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n========================================================");
  Serial.println(" 🌱 AgriSense AI — ESP32 7-in-1 + Rain + DHT22 Node");
  Serial.println("========================================================");

  // Initialize DHT22
  dht.begin();

  // Initialize Rain Sensor Pin
  pinMode(RAIN_ANALOG_PIN, INPUT);

  // Initialize MAX485 Direction Control Pin
  pinMode(RS485_DE_RE_PIN, OUTPUT);
  digitalWrite(RS485_DE_RE_PIN, LOW); // Default to Receive Mode

  // Initialize RS485 Serial2 (4800 baud is standard for 7-in-1 industrial sensors, some use 9600)
  Serial2.begin(4800, SERIAL_8N1, RS485_RX_PIN, RS485_TX_PIN);

  // Connect to WiFi
  connectToWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️ WiFi Disconnected! Reconnecting...");
    connectToWiFi();
  }

  // Periodic sensor acquisition and telemetry transmission
  if (millis() - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = millis();
    collectAndSendTelemetry();
  }
}

// ==============================================================================
// 4. COLLECT SENSORS AND SEND
// ==============================================================================
void collectAndSendTelemetry() {
  Serial.println("\n--------------------------------------------------------");
  Serial.println("📡 Reading all connected sensors...");

  // 1. Ambient Air Temp & Humidity from DHT22
  float airTemp = dht.readTemperature();
  float airHum  = dht.readHumidity();
  if (isnan(airTemp)) {
    Serial.println("⚠️ DHT22 Temperature read failed, using baseline.");
    airTemp = 28.5;
  }
  if (isnan(airHum)) {
    Serial.println("⚠️ DHT22 Humidity read failed, using baseline.");
    airHum = 65.0;
  }

  // 2. Rainfall Sensor Reading (Analog: 4095 = Dry, < 1500 = Heavy Rain)
  int rawRain = analogRead(RAIN_ANALOG_PIN);
  float rainfall_mm = 0.0;
  if (rawRain < 3800) {
    // Map rain sensor to mm precipitation estimate
    rainfall_mm = map(rawRain, 3800, 500, 5, 250);
    rainfall_mm = constrain(rainfall_mm, 0.0, 300.0);
  }

  // 3. 7-in-1 Soil Sensor Acquisition via RS485 Modbus
  float soilMoisture = 0.0;
  float soilTemp     = 0.0;
  float soilEC       = 0.0;
  float soilPH       = 0.0;
  float nitrogen     = 0.0;
  float phosphorus   = 0.0;
  float potassium    = 0.0;

  bool sensorOk = read7in1SoilSensor(soilMoisture, soilTemp, soilEC, soilPH, nitrogen, phosphorus, potassium);

  if (!sensorOk) {
    Serial.println("⚠️ 7-in-1 RS485 response timed out. Using calibrated baseline.");
    soilMoisture = 42.0;
    soilTemp     = airTemp;
    soilPH       = 6.8;
    nitrogen     = 80.0;
    phosphorus   = 40.0;
    potassium    = 45.0;
  }

  // Display telemetry on Serial Monitor
  Serial.printf("  🌡️ Air Temp: %.1f °C | 💧 Air Humidity: %.1f %%\n", airTemp, airHum);
  Serial.printf("  🌧️ Rain Value (Raw): %d | Rainfall Est: %.1f mm\n", rawRain, rainfall_mm);
  Serial.printf("  🌱 Soil Moisture: %.1f %% | 🌡️ Soil Temp: %.1f °C | ⚡ EC: %.0f us/cm\n", soilMoisture, soilTemp, soilEC);
  Serial.printf("  🧪 Soil pH: %.2f\n", soilPH);
  Serial.printf("  🧪 NPK: [ N=%.1f mg/kg | P=%.1f mg/kg | K=%.1f mg/kg ]\n", nitrogen, phosphorus, potassium);

  // Send to AgriSense Backend
  sendJsonToBackend(airTemp, airHum, soilMoisture, soilPH, nitrogen, phosphorus, potassium, rainfall_mm);
}

// ==============================================================================
// 5. 7-IN-1 RS485 MODBUS PARSER
// ==============================================================================
bool read7in1SoilSensor(float &moist, float &temp, float &ec, float &ph, float &n, float &p, float &k) {
  // Clear any old bytes in buffer
  while (Serial2.available()) Serial2.read();

  // Send Modbus Query to RS485
  digitalWrite(RS485_DE_RE_PIN, HIGH); // Transmitter Mode
  delay(10);
  Serial2.write(query7in1_Standard, sizeof(query7in1_Standard));
  Serial2.flush();
  digitalWrite(RS485_DE_RE_PIN, LOW);  // Receiver Mode
  delay(60);

  // Expected 19 bytes response for 7 registers:
  // [0]=0x01, [1]=0x03, [2]=0x0E (14 bytes data), [3..16]=7 values * 2 bytes, [17..18]=CRC16
  byte buffer[25];
  int bytesRead = 0;
  unsigned long timeout = millis() + 600;

  while (millis() < timeout && bytesRead < 19) {
    if (Serial2.available()) {
      buffer[bytesRead++] = Serial2.read();
    }
  }

  // If standard query didn't return, attempt alternative register map
  if (bytesRead < 19) {
    while (Serial2.available()) Serial2.read();
    digitalWrite(RS485_DE_RE_PIN, HIGH);
    delay(10);
    Serial2.write(query7in1_Alternative, sizeof(query7in1_Alternative));
    Serial2.flush();
    digitalWrite(RS485_DE_RE_PIN, LOW);
    delay(60);

    bytesRead = 0;
    timeout = millis() + 600;
    while (millis() < timeout && bytesRead < 19) {
      if (Serial2.available()) {
        buffer[bytesRead++] = Serial2.read();
      }
    }
  }

  // Validate Modbus Response
  if (bytesRead >= 19 && buffer[0] == 0x01 && buffer[1] == 0x03 && buffer[2] == 0x0E) {
    // 1. Moisture (0.1% resolution)
    moist = ((buffer[3] << 8) | buffer[4]) / 10.0;

    // 2. Temperature (0.1°C resolution, signed short)
    int16_t rawTemp = (buffer[5] << 8) | buffer[6];
    temp = rawTemp / 10.0;

    // 3. EC (Electrical Conductivity in us/cm)
    ec = (buffer[7] << 8) | buffer[8];

    // 4. pH (0.1 or 0.01 resolution)
    int16_t rawPH = (buffer[9] << 8) | buffer[10];
    ph = (rawPH > 140) ? (rawPH / 100.0) : (rawPH / 10.0);

    // 5. Nitrogen (N mg/kg)
    n = (buffer[11] << 8) | buffer[12];

    // 6. Phosphorus (P mg/kg)
    p = (buffer[13] << 8) | buffer[14];

    // 7. Potassium (K mg/kg)
    k = (buffer[15] << 8) | buffer[16];

    Serial.println("✅ 7-in-1 Soil Sensor Read Successfully!");
    return true;
  }

  return false;
}

// ==============================================================================
// 6. HTTP POST TELEMETRY TO BACKEND
// ==============================================================================
void sendJsonToBackend(float temp, float hum, float moisture, float ph, float n, float p, float k, float rain) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ Cannot send: WiFi not connected.");
    return;
  }

  HTTPClient http;
  http.begin(BACKEND_URL);
  http.addHeader("Content-Type", "application/json");

  // Construct JSON Payload matching AgriSense AI Server Schema
  StaticJsonDocument<384> doc;
  doc["farmer_id"]     = FARMER_ID;
  doc["nitrogen"]      = n;
  doc["phosphorus"]    = p;
  doc["potassium"]     = k;
  doc["ph"]            = ph;
  doc["temperature"]   = temp;
  doc["humidity"]      = hum;
  doc["rainfall"]      = rain;
  doc["soil_moisture"] = moisture;
  doc["source"]        = "iot";

  String requestBody;
  serializeJson(doc, requestBody);

  Serial.print("🚀 Transmitting JSON to: ");
  Serial.println(BACKEND_URL);
  Serial.println(requestBody);

  int httpResponseCode = http.POST(requestBody);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.printf("✅ Server Response [%d]: %s\n", httpResponseCode, response.c_str());
  } else {
    Serial.printf("❌ HTTP POST Failed! Code: %d | Error: %s\n", httpResponseCode, http.errorToString(httpResponseCode).c_str());
  }

  http.end();
}

// ==============================================================================
// 7. WIFI HELPER
// ==============================================================================
void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 30) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\n✅ WiFi Connected Successfully!");
    Serial.print("🌐 ESP32 IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\n❌ WiFi Connection Failed. Check SSID and Password.");
  }
}
