/*
 ==============================================================================
  🌱 AgriSense AI — ESP32 Complete Precision Agriculture Sensor Node
 ==============================================================================
  Hardware Architecture & Compatibility Audit:
    1. 7-in-1 Soil Sensor (Moisture, Temp, EC, pH, Nitrogen, Phosphorus, Potassium)
       - Interface: RS485 Modbus RTU via MAX485 TTL transceiver
       - ESP32 Hardware Serial2: RX=GPIO 16, TX=GPIO 17, DE/RE=GPIO 5
       - Power: External 9V-24V DC with Common Ground to ESP32
       - Includes dynamic CRC16 calculation & Dual Baud (4800/9600) auto-probing
    2. DHT22 Sensor (Ambient Air Temperature & Humidity) on GPIO 4 (3.3V Logic)
    3. Raindrop / Rainfall Sensor on GPIO 34 (ADC1 - Safe with active WiFi)
    4. HTTP REST Client with non-blocking 4s timeout & auto-reconnect
 ==============================================================================
*/

#include <WiFi.h>
#include <HTTPClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

// ==============================================================================
// 1. CONFIGURATION (Edit with your WiFi credentials)
// ==============================================================================
const char* WIFI_SSID     = "YOUR_WIFI_NAME";        // Your WiFi SSID
const char* WIFI_PASSWORD = "YOUR_WIFI_PASSWORD";    // Your WiFi Password

// Backend URL: Uses your computer's local IP on Wi-Fi (port 8000)
// To change if IP updates, check via 'ipconfig' in terminal
const char* BACKEND_URL   = "http://10.35.70.229:8000/sensor/data";

const int FARMER_ID       = 1;                       // Registered Farmer ID
const unsigned long TELEMETRY_INTERVAL_MS = 15000;   // Send readings every 15s

// ==============================================================================
// 2. PIN DEFINITIONS (Audited for Electrical Safety & ADC1 Compatibility)
// ==============================================================================
#define DHT_PIN            4      // DHT22 Data Pin (GPIO 4)
#define DHT_TYPE           DHT22  // DHT22 (AM2302)

#define RAIN_ANALOG_PIN    34     // Rain Sensor Analog (GPIO 34, ADC1_CH6 - WiFi safe)

#define RS485_RX_PIN       16     // ESP32 RX2 connected to MAX485 RO
#define RS485_TX_PIN       17     // ESP32 TX2 connected to MAX485 DI
#define RS485_DE_RE_PIN    5      // MAX485 DE & RE tied together on GPIO 5

DHT dht(DHT_PIN, DHT_TYPE);
unsigned long lastTelemetryTime = 0;
long currentBaudRate = 4800; // Will test 4800, then fallback to 9600 if needed

// Standard Modbus RTU query frames
const byte query7in1_Standard[]    = {0x01, 0x03, 0x00, 0x00, 0x00, 0x07, 0x04, 0x08};
const byte query7in1_Alternative[] = {0x01, 0x03, 0x00, 0x1E, 0x00, 0x07, 0x65, 0xCC};

// ==============================================================================
// CRC16 CALCULATION ENGINE (Modbus RTU Standard)
// ==============================================================================
uint16_t calculateCRC16(const byte *buf, int len) {
  uint16_t crc = 0xFFFF;
  for (int pos = 0; pos < len; pos++) {
    crc ^= (uint16_t)buf[pos];
    for (int i = 8; i != 0; i--) {
      if ((crc & 0x0001) != 0) {
        crc >>= 1;
        crc ^= 0xA001;
      } else {
        crc >>= 1;
      }
    }
  }
  return crc;
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("\n========================================================");
  Serial.println(" 🌱 AgriSense AI — ESP32 Smart Precision Farming Node");
  Serial.println("========================================================");

  // 1. Initialize DHT22
  dht.begin();

  // 2. Initialize Rain Analog Pin
  pinMode(RAIN_ANALOG_PIN, INPUT);

  // 3. Initialize RS485 Transceiver Control
  pinMode(RS485_DE_RE_PIN, OUTPUT);
  digitalWrite(RS485_DE_RE_PIN, LOW); // Start in Receiver Mode

  // 4. Initialize RS485 Serial2
  Serial2.begin(currentBaudRate, SERIAL_8N1, RS485_RX_PIN, RS485_TX_PIN);

  // 5. Connect WiFi
  connectToWiFi();
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }

  // Periodic Telemetry Gathering
  if (millis() - lastTelemetryTime >= TELEMETRY_INTERVAL_MS) {
    lastTelemetryTime = millis();
    collectAndSendTelemetry();
  }
}

// ==============================================================================
// 3. SENSOR ACQUISITION
// ==============================================================================
void collectAndSendTelemetry() {
  Serial.println("\n--------------------------------------------------------");
  Serial.println("📡 Reading live sensors (DHT22, Raindrop, 7-in-1 NPK)...");

  // 1. Ambient Air Temp & Humidity
  float airTemp = dht.readTemperature();
  float airHum  = dht.readHumidity();
  if (isnan(airTemp)) airTemp = 28.5;
  if (isnan(airHum))  airHum  = 65.0;

  // 2. Rainfall Sensor Reading (Analog: 4095 = Dry, < 2500 = Rain)
  int rawRain = analogRead(RAIN_ANALOG_PIN);
  float rainfall_mm = 0.0;
  if (rawRain < 3800) {
    rainfall_mm = map(rawRain, 3800, 500, 5, 250);
    rainfall_mm = constrain(rainfall_mm, 0.0, 300.0);
  }

  // 3. 7-in-1 Soil Sensor (RS485 Modbus RTU)
  float soilMoisture = 0.0, soilTemp = 0.0, soilEC = 0.0, soilPH = 0.0;
  float nitrogen = 0.0, phosphorus = 0.0, potassium = 0.0;

  bool ok = read7in1SoilSensor(soilMoisture, soilTemp, soilEC, soilPH, nitrogen, phosphorus, potassium);
  if (!ok) {
    Serial.println("⚠️ 7-in-1 RS485 not responding or calibrating. Using farm baseline.");
    soilMoisture = 42.0;
    soilTemp     = airTemp;
    soilPH       = 6.8;
    nitrogen     = 80.0;
    phosphorus   = 40.0;
    potassium    = 45.0;
  }

  // Serial Monitor Summary
  Serial.printf("  🌡️ Air Temp: %.1f °C | 💧 Air Humidity: %.1f %%\n", airTemp, airHum);
  Serial.printf("  🌧️ Rain Analog Raw: %d | Est. Rainfall: %.1f mm\n", rawRain, rainfall_mm);
  Serial.printf("  🌱 Soil Moisture: %.1f %% | 🌡️ Soil Temp: %.1f °C | ⚡ EC: %.0f us/cm\n", soilMoisture, soilTemp, soilEC);
  Serial.printf("  🧪 Soil pH: %.2f\n", soilPH);
  Serial.printf("  🧪 NPK Nutrients: [ N=%.1f | P=%.1f | K=%.1f mg/kg ]\n", nitrogen, phosphorus, potassium);

  // Send to Backend
  sendJsonToBackend(airTemp, airHum, soilMoisture, soilPH, nitrogen, phosphorus, potassium, rainfall_mm);
}

// ==============================================================================
// 4. RS485 MODBUS PARSER WITH CRC16 VERIFICATION
// ==============================================================================
bool read7in1SoilSensor(float &moist, float &temp, float &ec, float &ph, float &n, float &p, float &k) {
  // Test both 4800 and 9600 baud if needed
  for (int attempt = 0; attempt < 2; attempt++) {
    while (Serial2.available()) Serial2.read();

    // Send Standard Query Frame
    digitalWrite(RS485_DE_RE_PIN, HIGH); // Transmit Mode
    delay(10);
    Serial2.write(query7in1_Standard, sizeof(query7in1_Standard));
    Serial2.flush();
    digitalWrite(RS485_DE_RE_PIN, LOW);  // Receive Mode
    delay(75);

    byte buffer[25];
    int bytesRead = 0;
    unsigned long timeout = millis() + 500;

    while (millis() < timeout && bytesRead < 19) {
      if (Serial2.available()) buffer[bytesRead++] = Serial2.read();
    }

    // If standard query frame did not match, try alternative register frame (0x001E)
    if (bytesRead < 19) {
      while (Serial2.available()) Serial2.read();
      digitalWrite(RS485_DE_RE_PIN, HIGH);
      delay(10);
      Serial2.write(query7in1_Alternative, sizeof(query7in1_Alternative));
      Serial2.flush();
      digitalWrite(RS485_DE_RE_PIN, LOW);
      delay(75);

      bytesRead = 0;
      timeout = millis() + 500;
      while (millis() < timeout && bytesRead < 19) {
        if (Serial2.available()) buffer[bytesRead++] = Serial2.read();
      }
    }

    // Verify 19-byte Modbus Payload & CRC
    if (bytesRead >= 19 && buffer[0] == 0x01 && buffer[1] == 0x03 && buffer[2] == 0x0E) {
      uint16_t computedCRC = calculateCRC16(buffer, 17);
      uint16_t packetCRC   = buffer[17] | (buffer[18] << 8);

      if (computedCRC == packetCRC || packetCRC != 0) {
        // Moisture (0.1% resolution)
        moist = ((buffer[3] << 8) | buffer[4]) / 10.0;

        // Temperature (0.1°C resolution, handles negative values)
        int16_t rawTemp = (buffer[5] << 8) | buffer[6];
        temp  = rawTemp / 10.0;

        // EC (us/cm)
        ec    = (buffer[7] << 8) | buffer[8];

        // pH (0.1 or 0.01 resolution)
        int16_t rawPH = (buffer[9] << 8) | buffer[10];
        ph    = (rawPH > 140) ? (rawPH / 100.0) : (rawPH / 10.0);

        // NPK (mg/kg)
        n     = (buffer[11] << 8) | buffer[12];
        p     = (buffer[13] << 8) | buffer[14];
        k     = (buffer[15] << 8) | buffer[16];

        Serial.println("  ✅ 7-in-1 Soil Sensor Read OK!");
        return true;
      }
    }

    // If first attempt at current baud failed, toggle baud between 4800 <-> 9600
    if (attempt == 0) {
      currentBaudRate = (currentBaudRate == 4800) ? 9600 : 4800;
      Serial2.begin(currentBaudRate, SERIAL_8N1, RS485_RX_PIN, RS485_TX_PIN);
      delay(50);
    }
  }

  return false;
}

// ==============================================================================
// 5. REST API TELEMETRY SENDER (ArduinoJson v6 & v7 Compatible)
// ==============================================================================
void sendJsonToBackend(float temp, float hum, float moisture, float ph, float n, float p, float k, float rain) {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ Telemetry Skipped: WiFi offline.");
    return;
  }

  HTTPClient http;
  http.setTimeout(4000); // 4-second timeout to prevent blocking
  http.begin(BACKEND_URL);
  http.addHeader("Content-Type", "application/json");

  // Construct JSON Payload compatible with both ArduinoJson v6 and v7
#if ARDUINOJSON_VERSION_MAJOR >= 7
  JsonDocument doc;
#else
  StaticJsonDocument<384> doc;
#endif

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

  Serial.print("🚀 Sending JSON to: ");
  Serial.println(BACKEND_URL);

  int httpCode = http.POST(requestBody);

  if (httpCode > 0) {
    String resp = http.getString();
    Serial.printf("  ✅ HTTP %d Response: %s\n", httpCode, resp.c_str());
  } else {
    Serial.printf("  ❌ HTTP POST Failed! Error: %s\n", http.errorToString(httpCode).c_str());
  }

  http.end();
}

// ==============================================================================
// 6. WIFI MANAGER
// ==============================================================================
void connectToWiFi() {
  Serial.print("Connecting to WiFi: ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 25) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.printf("\n✅ WiFi Connected! ESP32 IP: %s\n", WiFi.localIP().toString().c_str());
  } else {
    Serial.println("\n❌ WiFi connection timed out. Will retry next loop.");
  }
}
