const API_BASE = "http://localhost:8000";

export const api = {
  // Server Health
  async checkHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`, { mode: "cors", cache: "no-store" });
      if (!res.ok) throw new Error("Health check failed");
      return await res.json();
    } catch (err) {
      console.warn("Backend offline:", err);
      return { status: "offline" };
    }
  },

  // Farmer Authentication
  async loginFarmer(name, phone, language = "English") {
    const res = await fetch(`${API_BASE}/farmer/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, phone, language }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Login failed" }));
      throw new Error(err.detail || "Login failed");
    }
    return await res.json();
  },

  async listFarmers() {
    const res = await fetch(`${API_BASE}/farmers`);
    if (!res.ok) return { status: "error", farmers: [] };
    return await res.json();
  },

  async getFarmerProfile(farmerId) {
    const res = await fetch(`${API_BASE}/farmer/${farmerId}`);
    if (!res.ok) throw new Error("Farmer not found");
    return await res.json();
  },

  // Farm Readings
  async getLatestFarmData(farmerId) {
    const res = await fetch(`${API_BASE}/farm/latest/${farmerId}`);
    if (!res.ok) return { status: "no_data" };
    return await res.json();
  },

  async getFarmHistory(farmerId, limit = 20) {
    const res = await fetch(`${API_BASE}/farm/history/${farmerId}?limit=${limit}`);
    if (!res.ok) return { status: "error", data: [] };
    return await res.json();
  },

  async saveManualFarmData(data) {
    const res = await fetch(`${API_BASE}/farm/manual`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to save manual reading");
    return await res.json();
  },

  async sendSensorData(data) {
    const res = await fetch(`${API_BASE}/sensor/data`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to send sensor packet");
    return await res.json();
  },

  async getSensorStatus(farmerId) {
    const res = await fetch(`${API_BASE}/sensor/status/${farmerId}`);
    if (!res.ok) return { status: "offline", connected: false };
    return await res.json();
  },

  // ML Crop Prediction
  async getLatestCrop(farmerId) {
    const res = await fetch(`${API_BASE}/crop/latest/${farmerId}`);
    if (!res.ok) return { status: "no_data" };
    return await res.json();
  },

  async predictCrop(data) {
    const res = await fetch(`${API_BASE}/crop/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Crop prediction failed" }));
      throw new Error(err.detail || "Prediction failed");
    }
    return await res.json();
  },

  async predictLatestCrop(farmerId) {
    const res = await fetch(`${API_BASE}/crop/predict-latest/${farmerId}`, {
      method: "POST",
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Prediction failed" }));
      throw new Error(err.detail || "Prediction failed");
    }
    return await res.json();
  },

  // AI Assistant Chat
  async askAiAssistant(farmerId, question, language = "English") {
    const res = await fetch(`${API_BASE}/ai/ask`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ farmer_id: farmerId, question, language }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "AI request failed" }));
      throw new Error(err.detail || "AI request failed");
    }
    return await res.json();
  },

  async askAi(farmerId, question, language = "English") {
    return this.askAiAssistant(farmerId, question, language);
  },

  // Disease Detection
  async detectPlantDisease(farmerId, crop, symptoms, imageBase64 = null, language = "English") {
    const res = await fetch(`${API_BASE}/disease/detect`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        farmer_id: farmerId,
        crop,
        symptoms,
        image_base64: imageBase64,
        language,
      }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Disease detection failed" }));
      throw new Error(err.detail || "Diagnosis failed");
    }
    return await res.json();
  },

  // WebSocket Live Voice URL Builder
  getLiveVoiceWebSocketUrl(farmerId, language = "English") {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = window.location.hostname || "localhost";
    return `${protocol}//${host}:8000/live?language=${encodeURIComponent(language)}&farmer_id=${encodeURIComponent(farmerId)}`;
  }
};
