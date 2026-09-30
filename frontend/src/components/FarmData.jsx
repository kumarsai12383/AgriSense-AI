import React, { useState, useEffect } from 'react';
import { Cpu, Send, RefreshCw, Clock, History, CheckCircle2, Wifi, Zap, PlusCircle } from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

export default function FarmData({ farmer, language, farmData, onDataUpdated, addToast }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const [activeTab, setActiveTab] = useState('manual'); // 'manual' | 'iot' | 'history'

  const [formData, setFormData] = useState({
    nitrogen: farmData?.nitrogen ?? 90,
    phosphorus: farmData?.phosphorus ?? 42,
    potassium: farmData?.potassium ?? 43,
    temperature: farmData?.temperature ?? 26.0,
    humidity: farmData?.humidity ?? 78.0,
    ph: farmData?.ph ?? 6.5,
    rainfall: farmData?.rainfall ?? 180.0,
    soil_moisture: farmData?.soil_moisture ?? 42.0,
  });

  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [autoPing, setAutoPing] = useState(false);

  // Load history
  const loadHistory = async () => {
    if (!farmer?.id) return;
    try {
      const res = await api.getFarmHistory(farmer.id, 15);
      if (res && res.data) {
        setHistory(res.data);
      }
    } catch (e) {
      console.warn('History load error:', e);
    }
  };

  useEffect(() => {
    loadHistory();
  }, [farmer?.id]);

  // Handle manual save
  const handleSaveManual = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = {
        farmer_id: farmer?.id || 1,
        nitrogen: parseFloat(formData.nitrogen),
        phosphorus: parseFloat(formData.phosphorus),
        potassium: parseFloat(formData.potassium),
        temperature: parseFloat(formData.temperature),
        humidity: parseFloat(formData.humidity),
        ph: parseFloat(formData.ph),
        rainfall: parseFloat(formData.rainfall),
        soil_moisture: parseFloat(formData.soil_moisture),
        source: 'manual'
      };

      const res = await api.saveManualFarmData(payload);
      if (res && res.status === 'success') {
        onDataUpdated(payload);
        loadHistory();
        addToast('Manual farm reading saved to database!', 'success');
      }
    } catch (err) {
      console.error(err);
      onDataUpdated(formData);
      addToast('Farm reading updated locally', 'info');
    } finally {
      setLoading(false);
    }
  };

  // Handle IoT packet broadcast
  const handleBroadcastIoT = async () => {
    setLoading(true);
    try {
      // Simulate realistic sensor fluctuations
      const jitter = (v, delta) => Math.round((v + (Math.random() * delta * 2 - delta)) * 10) / 10;
      const iotPacket = {
        farmer_id: farmer?.id || 1,
        nitrogen: jitter(formData.nitrogen, 4),
        phosphorus: jitter(formData.phosphorus, 2),
        potassium: jitter(formData.potassium, 3),
        temperature: jitter(formData.temperature, 1.5),
        humidity: jitter(formData.humidity, 3),
        ph: jitter(formData.ph, 0.2),
        rainfall: jitter(formData.rainfall, 5),
        soil_moisture: jitter(formData.soil_moisture, 2.5),
        source: 'iot'
      };

      const res = await api.sendSensorData(iotPacket);
      if (res && res.status === 'success') {
        onDataUpdated(iotPacket);
        setFormData(iotPacket);
        loadHistory();
        addToast(`📡 IoT Telemetry Packet Broadcasted! (Moisture: ${iotPacket.soil_moisture}%)`, 'success');
      }
    } catch (err) {
      console.error(err);
      addToast('IoT packet broadcast failed', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #475569 0%, #1e293b 100%)',
          color: 'white',
          padding: '24px 28px',
          borderRadius: 20
        }}
      >
        <h2 style={{ color: 'white', fontSize: 24, margin: '0 0 6px 0' }}>
          {t.sensors.title}
        </h2>
        <p style={{ color: '#cbd5e1', fontSize: 14, margin: 0, maxWidth: 650 }}>
          {t.sensors.subtitle}
        </p>
      </div>

      {/* Tabs */}
      <div style={{ display: 'flex', gap: 8, background: '#f1f5f9', padding: 6, borderRadius: 14, width: '100%', maxWidth: 420, flexWrap: 'wrap', boxSizing: 'border-box' }}>
        <button
          onClick={() => setActiveTab('manual')}
          style={{
            flex: '1 1 100px',
            padding: '10px 14px',
            borderRadius: 10,
            border: 'none',
            fontSize: 13,
            fontWeight: 800,
            cursor: 'pointer',
            textAlign: 'center',
            background: activeTab === 'manual' ? '#ffffff' : 'transparent',
            color: activeTab === 'manual' ? '#15803d' : '#64748b',
            boxShadow: activeTab === 'manual' ? '0 2px 8px rgba(0,0,0,0.06)' : 'none'
          }}
        >
          {t.sensors.manualTab}
        </button>

        <button
          onClick={() => setActiveTab('iot')}
          style={{
            flex: '1 1 100px',
            padding: '10px 14px',
            borderRadius: 10,
            border: 'none',
            fontSize: 13,
            fontWeight: 800,
            cursor: 'pointer',
            textAlign: 'center',
            background: activeTab === 'iot' ? '#ffffff' : 'transparent',
            color: activeTab === 'iot' ? '#15803d' : '#64748b',
            boxShadow: activeTab === 'iot' ? '0 2px 8px rgba(0,0,0,0.06)' : 'none'
          }}
        >
          {t.sensors.iotTab}
        </button>

        <button
          onClick={() => setActiveTab('history')}
          style={{
            flex: '1 1 100px',
            padding: '10px 14px',
            borderRadius: 10,
            border: 'none',
            fontSize: 13,
            fontWeight: 800,
            cursor: 'pointer',
            textAlign: 'center',
            background: activeTab === 'history' ? '#ffffff' : 'transparent',
            color: activeTab === 'history' ? '#15803d' : '#64748b',
            boxShadow: activeTab === 'history' ? '0 2px 8px rgba(0,0,0,0.06)' : 'none'
          }}
        >
          {t.sensors.historyTab}
        </button>
      </div>

      {/* Tab 1: Manual Farm Entry Form */}
      {activeTab === 'manual' && (
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <PlusCircle size={20} style={{ color: '#15803d' }} />
              <span>Record Soil Testing Lab / Field Measurements</span>
            </div>
          </div>

          <form onSubmit={handleSaveManual}>
            <div className="grid-4">
              <div className="input-group">
                <label className="input-label">Nitrogen (N)</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.nitrogen}
                  onChange={(e) => setFormData({ ...formData, nitrogen: e.target.value })}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Phosphorus (P)</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.phosphorus}
                  onChange={(e) => setFormData({ ...formData, phosphorus: e.target.value })}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Potassium (K)</label>
                <input
                  type="number"
                  className="input-field"
                  value={formData.potassium}
                  onChange={(e) => setFormData({ ...formData, potassium: e.target.value })}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Soil pH</label>
                <input
                  type="number"
                  step="0.1"
                  className="input-field"
                  value={formData.ph}
                  onChange={(e) => setFormData({ ...formData, ph: e.target.value })}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Temperature (°C)</label>
                <input
                  type="number"
                  step="0.1"
                  className="input-field"
                  value={formData.temperature}
                  onChange={(e) => setFormData({ ...formData, temperature: e.target.value })}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Humidity (%)</label>
                <input
                  type="number"
                  step="0.1"
                  className="input-field"
                  value={formData.humidity}
                  onChange={(e) => setFormData({ ...formData, humidity: e.target.value })}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Rainfall (mm)</label>
                <input
                  type="number"
                  step="0.1"
                  className="input-field"
                  value={formData.rainfall}
                  onChange={(e) => setFormData({ ...formData, rainfall: e.target.value })}
                  required
                />
              </div>

              <div className="input-group">
                <label className="input-label">Soil Moisture (%)</label>
                <input
                  type="number"
                  step="0.1"
                  className="input-field"
                  value={formData.soil_moisture}
                  onChange={(e) => setFormData({ ...formData, soil_moisture: e.target.value })}
                  required
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="btn btn-primary"
              style={{ marginTop: 12, height: 46 }}
            >
              <span>{t.sensors.saveBtn}</span>
            </button>
          </form>
        </div>
      )}

      {/* Tab 2: IoT Telemetry Simulator */}
      {activeTab === 'iot' && (
        <div className="agri-card" style={{ maxWidth: 700 }}>
          <div className="agri-card-header">
            <div className="agri-card-title">
              <Cpu size={20} style={{ color: '#7e22ce' }} />
              <span>RS485 / Modbus 7-in-1 IoT Soil Probe Simulator</span>
            </div>
            <span className="badge badge-green">Device Connected</span>
          </div>

          <p style={{ fontSize: 14, color: '#334155', lineHeight: 1.5, marginBottom: 20 }}>
            Broadcasts a live hardware telemetry packet with NPK, EC, soil moisture, pH, and ambient weather directly to the backend <code>/sensor/data</code> endpoint.
          </p>

          <button
            onClick={handleBroadcastIoT}
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', height: 48, fontSize: 16 }}
          >
            <Wifi size={18} />
            <span>{t.sensors.broadcastBtn}</span>
          </button>
        </div>
      )}

      {/* Tab 3: History Log */}
      {activeTab === 'history' && (
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <History size={20} style={{ color: '#15803d' }} />
              <span>Historical Sensor & Soil Reading Logs</span>
            </div>
            <button onClick={loadHistory} className="btn btn-secondary" style={{ padding: '6px 12px' }}>
              <RefreshCw size={14} />
              <span>Refresh</span>
            </button>
          </div>

          {history.length > 0 ? (
            <div className="table-responsive-container">
              <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: 13, minWidth: 500 }}>
                <thead>
                  <tr style={{ background: '#f8fafc', borderBottom: '2px solid #e2e8f0', textAlign: 'left' }}>
                    <th style={{ padding: '10px 12px' }}>Timestamp</th>
                    <th style={{ padding: '10px 12px' }}>Source</th>
                    <th style={{ padding: '10px 12px' }}>NPK (kg/ha)</th>
                    <th style={{ padding: '10px 12px' }}>pH</th>
                    <th style={{ padding: '10px 12px' }}>Temp / Hum</th>
                    <th style={{ padding: '10px 12px' }}>Rainfall</th>
                    <th style={{ padding: '10px 12px' }}>Moisture</th>
                  </tr>
                </thead>
                <tbody>
                  {history.map((row, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid #f1f5f9' }}>
                      <td style={{ padding: '10px 12px', color: '#64748b' }}>
                        {row.date ? new Date(row.date).toLocaleString() : 'Recent'}
                      </td>
                      <td style={{ padding: '10px 12px' }}>
                        <span className={`badge ${row.source === 'iot' ? 'badge-blue' : 'badge-green'}`}>
                          {row.source || 'manual'}
                        </span>
                      </td>
                      <td style={{ padding: '10px 12px', fontWeight: 700, color: '#0f172a' }}>
                        {row.nitrogen}-{row.phosphorus}-{row.potassium}
                      </td>
                      <td style={{ padding: '10px 12px' }}>{row.ph}</td>
                      <td style={{ padding: '10px 12px' }}>{row.temperature}°C / {row.humidity}%</td>
                      <td style={{ padding: '10px 12px' }}>{row.rainfall} mm</td>
                      <td style={{ padding: '10px 12px', fontWeight: 700, color: '#0284c7' }}>
                        {row.soil_moisture ?? 38}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div style={{ textAlign: 'center', padding: '40px 20px', color: '#64748b' }}>
              No previous readings found. Save a reading above to build your farm record.
            </div>
          )}
        </div>
      )}
    </div>
  );
}
