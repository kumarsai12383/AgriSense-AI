import React, { useState } from 'react';
import { Droplets, Clock, CloudSun, AlertTriangle, CheckCircle2, Calendar, Gauge } from 'lucide-react';
import { TRANSLATIONS } from '../translations';

export default function IrrigationAdvisor({ farmData, language, latestCrop }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;

  const [acreage, setAcreage] = useState(2.5);
  const [cropType, setCropType] = useState(latestCrop?.crop || 'rice');
  const [soilType, setSoilType] = useState('Clay Loam');

  const moisture = farmData?.soil_moisture ?? 38;
  const temp = farmData?.temperature ?? 28;

  // Water calculation formula (liters per day)
  const calculateWaterRequirement = () => {
    const cropFactor = cropType === 'rice' ? 1.4 : cropType === 'cotton' ? 1.1 : cropType === 'banana' ? 1.5 : 0.9;
    const et0 = (temp * 0.2) + 2.5; // Estimated evapotranspiration (mm/day)
    const mmRequired = Math.max(10, (50 - moisture) * 0.8 + et0 * cropFactor);
    const totalLiters = Math.round(mmRequired * acreage * 4046.86); // 1 mm per acre ~ 4047 liters
    return { mmRequired: Math.round(mmRequired), totalLiters };
  };

  const { mmRequired, totalLiters } = calculateWaterRequirement();
  const isDry = moisture < 35;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #0284c7 0%, #0369a1 100%)',
          color: 'white',
          padding: '24px 28px',
          borderRadius: 20
        }}
      >
        <h2 style={{ color: 'white', fontSize: 24, margin: '0 0 6px 0' }}>
          {t.irrigation.title}
        </h2>
        <p style={{ color: '#e0f2fe', fontSize: 14, margin: 0, maxWidth: 650 }}>
          {t.irrigation.subtitle}
        </p>
      </div>

      <div className="grid-2">
        {/* Left: Real-time Moisture & Schedule */}
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <Droplets size={20} style={{ color: '#0284c7' }} />
              <span>Root Zone Moisture & Scheduling</span>
            </div>
            <span className={`badge ${isDry ? 'badge-amber' : 'badge-green'}`}>
              {isDry ? "Irrigation Recommended" : "Adequate Moisture"}
            </span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: 20, margin: '14px 0 20px 0' }}>
            <div style={{
              width: 80,
              height: 80,
              borderRadius: '50%',
              background: isDry ? 'linear-gradient(135deg, #f59e0b, #d97706)' : 'linear-gradient(135deg, #0284c7, #0369a1)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: 26,
              fontWeight: 800,
              boxShadow: '0 8px 20px rgba(2, 132, 199, 0.3)'
            }}>
              {Math.round(moisture)}%
            </div>
            <div>
              <div style={{ fontSize: 17, fontWeight: 800, color: '#0f172a' }}>
                {isDry ? "Soil Moisture Depleted" : "Optimal Field Capacity"}
              </div>
              <div style={{ fontSize: 13, color: '#64748b', marginTop: 3 }}>
                Permanent Wilting Point: 18% • Field Capacity: 45%
              </div>
            </div>
          </div>

          {/* Schedule Box */}
          <div style={{ background: '#f8fafc', padding: 16, borderRadius: 14, border: '1px solid #e2e8f0' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 14, fontWeight: 800, color: '#0f172a', marginBottom: 8 }}>
              <Clock size={16} style={{ color: '#0284c7' }} />
              <span>Recommended Watering Window:</span>
            </div>
            <div style={{ fontSize: 13, color: '#334155', lineHeight: 1.6 }}>
              ⏱ <strong>Best Time:</strong> Early Morning (5:30 AM – 8:30 AM) or Late Evening.<br />
              💧 <strong>Water Depth:</strong> Apply <strong>{mmRequired} mm</strong> ({totalLiters.toLocaleString()} Liters for {acreage} acres).<br />
              ⏳ <strong>Method:</strong> Drip / Furrow irrigation to minimize evaporation losses.
            </div>
          </div>
        </div>

        {/* Right: Water Budget Calculator */}
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <Gauge size={20} style={{ color: '#0284c7' }} />
              <span>Field Water Budget Calculator</span>
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">Land Size (Acres)</label>
            <input
              type="number"
              step="0.5"
              min="0.5"
              max="100"
              className="input-field"
              value={acreage}
              onChange={(e) => setAcreage(parseFloat(e.target.value) || 1)}
            />
          </div>

          <div className="input-group">
            <label className="input-label">Current Crop</label>
            <select
              className="input-field"
              value={cropType}
              onChange={(e) => setCropType(e.target.value)}
            >
              <option value="rice">Rice / Paddy (High Demand)</option>
              <option value="cotton">Cotton (Moderate Demand)</option>
              <option value="maize">Maize / Corn (Moderate Demand)</option>
              <option value="banana">Banana (High Demand)</option>
              <option value="chickpea">Chickpea / Bengal Gram (Low Demand)</option>
              <option value="pigeonpeas">Pigeon Pea / Tur (Low Demand)</option>
              <option value="watermelon">Watermelon (Moderate Demand)</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Soil Texture</label>
            <select
              className="input-field"
              value={soilType}
              onChange={(e) => setSoilType(e.target.value)}
            >
              <option value="Clay Loam">Clay Loam (High Retention)</option>
              <option value="Sandy Loam">Sandy Loam (Fast Drainage)</option>
              <option value="Black Cotton">Black Vertisol (Deep Retention)</option>
              <option value="Red Sandy">Red Sandy Loam</option>
            </select>
          </div>

          <div style={{ background: '#e0f2fe', padding: 14, borderRadius: 12, border: '1px solid #bae6fd', marginTop: 10 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <div>
                <div style={{ fontSize: 12, fontWeight: 700, color: '#0369a1' }}>Calculated Water Budget</div>
                <div style={{ fontSize: 20, fontWeight: 800, color: '#0c4a6e' }}>{totalLiters.toLocaleString()} Liters</div>
              </div>
              <span className="badge badge-blue">{mmRequired} mm / acre</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
