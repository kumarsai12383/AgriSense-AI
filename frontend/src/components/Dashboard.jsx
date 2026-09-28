import React, { useState } from 'react';
import {
  Sun, Droplets, Wheat, Activity, Sparkles, ArrowRight, Mic,
  Cpu, Stethoscope, TrendingUp, CheckCircle2, AlertTriangle,
  Volume2, Square, Building2, HelpCircle, Calculator, Layers,
  ChevronRight, FlaskConical, Leaf, Zap
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { CROPS_DATA } from '../cropData';

import DailyBriefing from './DailyBriefing';

// High-quality agriculture images (Unsplash direct CDN)
const HERO_IMAGES = [
  'https://images.unsplash.com/photo-1500937386664-56d1dfef3854?w=1600&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1574943320219-553eb213f72d?w=1600&auto=format&fit=crop&q=80',
  'https://images.unsplash.com/photo-1523348837708-15d4a09cfac2?w=1600&auto=format&fit=crop&q=80',
];

export default function Dashboard({
  farmer, language, farmData, latestCrop,
  setCurrentTab, sensorStatus, onAutofillAndPredict,
  onDataUpdated, addToast
}) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const cropInfo = latestCrop?.crop ? CROPS_DATA[latestCrop.crop.toLowerCase()] : null;
  const [heroImg] = useState(HERO_IMAGES[0]);

  // Soil health score
  const calculateSoilHealth = () => {
    if (!farmData) return 72;
    let s = 45;
    if (farmData.ph >= 6.0 && farmData.ph <= 7.5) s += 22;
    else if (farmData.ph >= 5.5 && farmData.ph <= 8.5) s += 11;
    if (farmData.nitrogen >= 40 && farmData.nitrogen <= 120) s += 11;
    if (farmData.phosphorus >= 30 && farmData.phosphorus <= 80) s += 11;
    if (farmData.potassium >= 30 && farmData.potassium <= 80) s += 11;
    return Math.min(100, Math.max(30, s));
  };

  const healthScore   = calculateSoilHealth();
  const soilMoisture  = farmData?.soil_moisture ?? 38;
  const isMoistureLow = soilMoisture < 30;
  const temp          = farmData?.temperature ?? 28;
  const ph            = farmData?.ph ?? 6.8;
  const farmerName    = farmer?.name || 'Farmer';

  const feats = t.dashboard?.features || {};
  const steps = t.dashboard?.steps || {};

  const featureGrid = [
    {
      id: 'sensors',
      icon: '📡', color: 'teal',
      iconBg: '#f0fdfa', iconColor: '#0f766e',
      title: feats.sensors?.title || 'Step 1 — Soil Test',
      desc: feats.sensors?.desc || 'Enter NPK, pH, moisture manually or connect the ESP32 7-in-1 sensor probe for live data.',
      cta: feats.sensors?.cta || 'Start Soil Test',
    },
    {
      id: 'crop',
      icon: '🌾', color: 'green',
      iconBg: '#f0fdf4', iconColor: '#15803d',
      title: feats.crop?.title || 'Step 2 — Crop AI Recommendation',
      desc: feats.crop?.desc || 'ML RandomForest model analyses your 7 soil & climate values to predict the best crop with alternatives.',
      cta: feats.crop?.cta || 'Get Crop Recommendation',
    },
    {
      id: 'soil',
      icon: '🧪', color: 'amber',
      iconBg: '#fef3c7', iconColor: '#b45309',
      title: feats.soil?.title || 'Soil Health Report',
      desc: feats.soil?.desc || 'Detailed NPK deficiency chart, pH chemistry, and personalized soil enrichment treatment plan.',
      cta: feats.soil?.cta || 'View Soil Report',
    },
    {
      id: 'irrigation',
      icon: '💧', color: 'blue',
      iconBg: '#e0f2fe', iconColor: '#0369a1',
      title: feats.irrigation?.title || 'Smart Irrigation',
      desc: feats.irrigation?.desc || 'Red = water urgently, Green = soil moist. Calculates exact motor pump hours for your field size.',
      cta: feats.irrigation?.cta || 'Open Irrigation Advisor',
    },
    {
      id: 'fertilizer',
      icon: '🌿', color: 'green',
      iconBg: '#f0fdf4', iconColor: '#15803d',
      title: feats.fertilizer?.title || 'Fertilizer Schedule',
      desc: feats.fertilizer?.desc || 'Stage-wise Urea, DAP, MOP bag quantities across 4 crop growth stages to minimize cost.',
      cta: feats.fertilizer?.cta || 'View Fertilizer Plan',
    },
    {
      id: 'disease',
      icon: '🔬', color: 'red',
      iconBg: '#fee2e2', iconColor: '#b91c1c',
      title: feats.disease?.title || 'Plant Doctor (AI)',
      desc: feats.disease?.desc || 'Upload a leaf photo or describe symptoms — AI diagnoses disease and gives organic + chemical cure.',
      cta: feats.disease?.cta || 'Open Plant Doctor',
    },
    {
      id: 'mandi',
      icon: '📊', color: 'purple',
      iconBg: '#f5f3ff', iconColor: '#7c3aed',
      title: feats.mandi?.title || 'Live Mandi Prices',
      desc: feats.mandi?.desc || 'e-NAM APMC rates, MSP comparison, best market timing, and full farm cost-profit estimator.',
      cta: feats.mandi?.cta || 'View Market Prices',
    },
    {
      id: 'schemes',
      icon: '🏛️', color: 'teal',
      iconBg: '#f0fdfa', iconColor: '#0f766e',
      title: feats.schemes?.title || 'Government Schemes',
      desc: feats.schemes?.desc || 'PM-KISAN ₹6,000 / PM-KUSUM solar pump / PMFBY insurance / KCC credit and 20+ state schemes.',
      cta: feats.schemes?.cta || 'Browse Schemes',
    },
    {
      id: 'voice',
      icon: '🎙️', color: 'green',
      iconBg: '#f0fdf4', iconColor: '#15803d',
      title: feats.voice?.title || 'Voice AI Assistant',
      desc: feats.voice?.desc || 'Speak in your language — AgriSense AI answers instantly with voice. Zero typing needed.',
      cta: feats.voice?.cta || 'Talk to AgriSense',
    },
    {
      id: 'chat',
      icon: '💬', color: 'blue',
      iconBg: '#e0f2fe', iconColor: '#0369a1',
      title: feats.chat?.title || 'AI Chat Assistant',
      desc: feats.chat?.desc || 'Ask any farming question by text. AI uses your actual farm data to give personalised advice.',
      cta: feats.chat?.cta || 'Open AI Chat',
    },
    {
      id: 'help',
      icon: '📖', color: 'purple',
      iconBg: '#f5f3ff', iconColor: '#7c3aed',
      title: feats.help?.title || 'Help & Guide',
      desc: feats.help?.desc || '7-step audio walkthrough, colour guide, best practices, and toll-free Kisan Helpline 1551.',
      cta: feats.help?.cta || 'Open Help Guide',
    },
  ];

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>

      {/* ══════════════════════════════════════════════
          HERO BANNER — AGRICULTURE BACKGROUND
          ══════════════════════════════════════════════ */}
      <div className="hero-banner">
        <div
          className="hero-bg"
          style={{ backgroundImage: `linear-gradient(175deg, rgba(5,46,22,0.30) 0%, rgba(5,46,22,0.82) 100%), url('${heroImg}')` }}
        />
        <div className="hero-pattern" />

        <div className="hero-content">
          {/* Welcome pill */}
          <div style={{
            display: 'inline-flex', alignItems: 'center', gap: 7,
            background: 'rgba(255,255,255,0.18)', border: '1.5px solid rgba(255,255,255,0.30)',
            padding: '5px 14px', borderRadius: 99, fontSize: 12, fontWeight: 800,
            color: 'rgba(255,255,255,0.92)', marginBottom: 14, backdropFilter: 'blur(6px)',
            textTransform: 'uppercase', letterSpacing: '0.5px'
          }}>
            <Sparkles size={13} />
            AgriSense AI v2.0 — {t.tagline || "Smart Agricultural Decision Support & Farm Intelligence"}
          </div>

          <h1 style={{
            color: 'white', fontSize: 'clamp(22px, 4vw, 36px)',
            fontWeight: 900, marginBottom: 8, lineHeight: 1.2, fontFamily: 'Outfit, sans-serif'
          }}>
            {t.dashboard?.welcome || 'Welcome back'}, {farmerName}! 🌾
          </h1>

          <p style={{ color: 'rgba(255,255,255,0.88)', fontSize: 15, fontWeight: 500, marginBottom: 20, maxWidth: 600 }}>
            {t.dashboard?.greeting || 'Your AI-powered farm intelligence platform for better yields, smarter decisions, and higher profits.'}
          </p>

          {/* Workflow Step Buttons */}
          <div className="workflow-steps">
            <button className={`workflow-step ${!farmData ? 'active' : ''}`} onClick={() => setCurrentTab('sensors')}>
              <span>📡</span> {steps.step1 || '1. Soil Test'}
            </button>
            <span className="workflow-arrow">›</span>
            <button className={`workflow-step ${farmData && !latestCrop ? 'active' : ''}`} onClick={() => setCurrentTab('crop')}>
              <span>🌾</span> {steps.step2 || '2. AI Recommendation'}
            </button>
            <span className="workflow-arrow">›</span>
            <button className={`workflow-step ${latestCrop ? 'active' : ''}`} onClick={() => setCurrentTab('crop')}>
              <span>📋</span> {steps.step3 || '3. Advice & Economics'}
            </button>
            <span className="workflow-arrow">›</span>
            <button className="workflow-step" onClick={() => setCurrentTab('irrigation')}>
              <span>💧</span> {t.nav?.irrigation || 'Irrigation'}
            </button>
          </div>

          {/* Quick CTA buttons */}
          <div style={{ display: 'flex', gap: 10, marginTop: 20, flexWrap: 'wrap' }}>
            <button
              id="btn-start-soil-test"
              onClick={() => setCurrentTab('sensors')}
              className="btn"
              style={{
                background: '#ffffff',
                color: '#15803d',
                fontWeight: 900,
                fontSize: 14,
                boxShadow: '0 6px 16px rgba(0,0,0,0.15)'
              }}
            >
              <Cpu size={16} />
              {feats.sensors?.cta || 'Start Soil Test'}
            </button>
            <button
              id="btn-get-crop-ai"
              onClick={() => setCurrentTab('crop')}
              className="btn"
              style={{
                background: 'linear-gradient(135deg, #16a34a, #22c55e)',
                color: '#ffffff',
                fontWeight: 900,
                fontSize: 14,
                border: '1px solid rgba(255,255,255,0.4)',
                boxShadow: '0 6px 16px rgba(22,163,74,0.35)'
              }}
            >
              <Wheat size={16} />
              {feats.crop?.cta || 'Get Crop Recommendation'}
            </button>
            <button
              id="btn-voice-ai"
              onClick={() => setCurrentTab('voice')}
              className="btn btn-ghost"
              style={{
                background: 'rgba(255,255,255,0.20)',
                color: '#ffffff',
                fontWeight: 800,
                fontSize: 14,
                border: '1px solid rgba(255,255,255,0.35)',
                backdropFilter: 'blur(8px)'
              }}
            >
              <Mic size={16} />
              {feats.voice?.cta || 'Talk to AI'}
            </button>
          </div>

          {/* Live Telemetry Ribbon (Pro Agro-Tech Header) */}
          <div className="telemetry-ribbon">
            <div className="telemetry-ribbon-item">
              <span className="telemetry-ribbon-label">🌡️ Soil Temp</span>
              <span className="telemetry-ribbon-value">{temp}°C</span>
            </div>
            <div className="telemetry-ribbon-item">
              <span className="telemetry-ribbon-label">💧 Moisture</span>
              <span className="telemetry-ribbon-value" style={{ color: isMoistureLow ? '#f87171' : '#4ade80' }}>
                {soilMoisture}% {isMoistureLow ? '⚠️ Low' : '✅ Optimal'}
              </span>
            </div>
            <div className="telemetry-ribbon-item">
              <span className="telemetry-ribbon-label">🧪 Soil pH</span>
              <span className="telemetry-ribbon-value">{ph} pH</span>
            </div>
            <div className="telemetry-ribbon-item">
              <span className="telemetry-ribbon-label">🌱 Soil Health</span>
              <span className="telemetry-ribbon-value" style={{ color: '#4ade80' }}>{healthScore}/100</span>
            </div>
            <div className="telemetry-ribbon-item">
              <span className="telemetry-ribbon-label">🛰️ Sensor Status</span>
              <span className="telemetry-ribbon-value">{sensorStatus ? '🟢 7-in-1 IoT Live' : '🔵 Manual Telemetry'}</span>
            </div>
          </div>
        </div>
      </div>

      {/* ══════════════════════════════════════════════
          DAILY 1-MINUTE FARM AUDIO BRIEFING
          ══════════════════════════════════════════════ */}
      <DailyBriefing
        farmer={farmer}
        language={language}
        farmData={farmData}
        latestCrop={latestCrop}
        onDataUpdated={onDataUpdated}
        addToast={addToast}
      />

      {/* ══════════════════════════════════════════════
          REAL-TIME METRIC CARDS
          ══════════════════════════════════════════════ */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))', gap: 16 }}>
        {/* Soil Score */}
        <div className="agri-card-pro" style={{ padding: 22 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: 12.5, fontWeight: 800, color: '#64748b' }}>{t.dashboard?.soilScore || 'Soil Health Index'}</span>
            <div style={{ padding: 8, background: '#f0fdf4', borderRadius: 12, color: '#15803d' }}>
              <Activity size={18} />
            </div>
          </div>
          <div style={{ fontSize: 32, fontWeight: 900, color: '#15803d', marginBottom: 8, fontFamily: 'Outfit, sans-serif' }}>
            {healthScore}<span style={{ fontSize: 14, color: '#64748b', fontWeight: 700 }}>/100</span>
          </div>
          <div className="soil-gauge">
            <div className="soil-gauge-fill" style={{
              width: `${healthScore}%`,
              background: `linear-gradient(90deg, ${healthScore > 70 ? '#22c55e' : healthScore > 50 ? '#eab308' : '#ef4444'}, ${healthScore > 70 ? '#15803d' : healthScore > 50 ? '#d97706' : '#dc2626'})`
            }} />
          </div>
          <span style={{ fontSize: 11.5, color: '#059669', fontWeight: 700, marginTop: 8, display: 'block' }}>
            {healthScore >= 80 ? '🌟 Excellent soil condition' : healthScore >= 60 ? '✅ Good soil, minor adjustments' : '⚠️ Soil needs enrichment'}
          </span>
        </div>

        {/* Moisture */}
        <div className="agri-card-pro" style={{ padding: 22 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: 12.5, fontWeight: 800, color: '#64748b' }}>{t.dashboard?.waterStatus || 'Soil Moisture'}</span>
            <div style={{ padding: 8, background: isMoistureLow ? '#fee2e2' : '#e0f2fe', borderRadius: 12, color: isMoistureLow ? '#dc2626' : '#0369a1' }}>
              <Droplets size={18} />
            </div>
          </div>
          <div style={{ fontSize: 32, fontWeight: 900, color: isMoistureLow ? '#dc2626' : '#0369a1', marginBottom: 8, fontFamily: 'Outfit, sans-serif' }}>
            {soilMoisture}%
          </div>
          <div className="soil-gauge">
            <div className="soil-gauge-fill" style={{
              width: `${Math.min(100, soilMoisture * 1.5)}%`,
              background: isMoistureLow ? '#ef4444' : '#0284c7'
            }} />
          </div>
          <span style={{ fontSize: 11.5, color: isMoistureLow ? '#dc2626' : '#0369a1', fontWeight: 800, marginTop: 8, display: 'block' }}>
            {isMoistureLow ? `⚠️ ${t.dashboard?.needsWater || 'Water needed urgently!'}` : `✅ ${t.dashboard?.optimal || 'Moisture optimal'}`}
          </span>
        </div>

        {/* Temperature */}
        <div className="agri-card-pro" style={{ padding: 22 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: 12.5, fontWeight: 800, color: '#64748b' }}>Ambient Climate</span>
            <div style={{ padding: 8, background: '#fef3c7', borderRadius: 12, color: '#d97706' }}>
              <Sun size={18} />
            </div>
          </div>
          <div style={{ fontSize: 32, fontWeight: 900, color: '#d97706', marginBottom: 8, fontFamily: 'Outfit, sans-serif' }}>
            {temp}°C
          </div>
          <div className="soil-gauge">
            <div className="soil-gauge-fill" style={{ width: `${Math.min(100, (temp / 45) * 100)}%`, background: '#f59e0b' }} />
          </div>
          <span style={{ fontSize: 11.5, color: '#92400e', fontWeight: 700, marginTop: 8, display: 'block' }}>
            💨 Humidity: {farmData?.humidity ?? 65}% • 🌧 Rain: {farmData?.rainfall ?? 110}mm
          </span>
        </div>

        {/* IoT Sensor */}
        <div className="agri-card-pro" style={{ padding: 22 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
            <span style={{ fontSize: 12.5, fontWeight: 800, color: '#64748b' }}>{t.dashboard?.iotStatus || 'IoT 7-in-1 Sensor'}</span>
            <div style={{ padding: 8, background: '#f5f3ff', borderRadius: 12, color: '#7c3aed' }}>
              <Cpu size={18} />
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
            <span className={`status-indicator ${sensorStatus ? 'status-online' : 'status-offline'}`} />
            <span style={{ fontSize: 14, fontWeight: 800, color: '#1e293b' }}>
              {sensorStatus ? 'ESP32 Live' : 'Manual Mode'}
            </span>
          </div>
          <div style={{ fontSize: 11, color: '#64748b', marginBottom: 10 }}>7-in-1: N, P, K, pH, Moisture, Temp, Humidity</div>
          <button
            id="btn-manage-sensors"
            onClick={() => setCurrentTab('sensors')}
            className="btn btn-secondary"
            style={{ padding: '6px 12px', fontSize: 11, width: '100%' }}
          >
            <span>Manage Sensors →</span>
          </button>
        </div>
      </div>

      {/* ══════════════════════════════════════════════
          LATEST CROP RECOMMENDATION CARD
          ══════════════════════════════════════════════ */}
      {latestCrop?.crop ? (
        <div className="agri-card" style={{
          background: 'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
          border: '2px solid #86efac', borderRadius: 24, padding: 24
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 16 }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
              <div style={{
                width: 72, height: 72, borderRadius: 20,
                background: 'linear-gradient(135deg, #15803d, #22c55e)',
                color: 'white', display: 'flex', alignItems: 'center',
                justifyContent: 'center', fontSize: 36,
                boxShadow: '0 8px 20px rgba(21,128,61,0.30)'
              }}>
                {cropInfo?.emoji || '🌾'}
              </div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 4 }}>
                  <CheckCircle2 size={14} color="#15803d" />
                  <span style={{ fontSize: 11, fontWeight: 800, color: '#15803d', textTransform: 'uppercase', letterSpacing: '0.5px' }}>
                    AI Recommended for Your Soil
                  </span>
                </div>
                <h2 style={{
                  fontSize: 28, fontWeight: 900, color: '#14532d',
                  margin: '0 0 4px 0', textTransform: 'capitalize', fontFamily: 'Outfit, sans-serif'
                }}>
                  {latestCrop.crop}
                </h2>
                <div style={{ fontSize: 13, color: '#166534', fontWeight: 600 }}>
                  {cropInfo?.category || 'Recommended Crop'} • Yield: <strong>{cropInfo?.yield || '4–6 T/ha'}</strong>
                  {' '}• Season: <strong>{cropInfo?.season || 'Kharif/Rabi'}</strong>
                </div>
              </div>
            </div>

            <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap' }}>
              <button
                id="btn-view-crop-details"
                onClick={() => setCurrentTab('crop')}
                className="btn btn-primary"
                style={{ padding: '11px 20px', borderRadius: 12 }}
              >
                <span>Full Crop Advice</span>
                <ArrowRight size={16} />
              </button>
              <button
                id="btn-crop-fertilizer"
                onClick={() => setCurrentTab('fertilizer')}
                className="btn btn-secondary"
                style={{ padding: '11px 18px', borderRadius: 12 }}
              >
                <FlaskConical size={15} />
                <span>Fertilizer Plan</span>
              </button>
            </div>
          </div>

          {/* Crop quick stats */}
          {cropInfo && (
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(150px, 1fr))', gap: 10, marginTop: 16 }}>
              {[
                { label: 'Duration', value: cropInfo.duration || '110-145 days', icon: '📅' },
                { label: 'Water Need', value: cropInfo.water?.split('.')[0] || 'Moderate', icon: '💧' },
                { label: 'NPK Ratio', value: cropInfo.npkRatio || '100:50:50 kg/ha', icon: '🧪' },
                { label: 'Soil pH', value: cropInfo.phRange || '6.0–7.5', icon: '⚗️' },
              ].map((stat, i) => (
                <div key={i} style={{
                  background: 'rgba(255,255,255,0.7)', padding: '10px 14px',
                  borderRadius: 12, border: '1px solid #bbf7d0'
                }}>
                  <div style={{ fontSize: 12, color: '#64748b', fontWeight: 600 }}>{stat.icon} {stat.label}</div>
                  <div style={{ fontSize: 13, fontWeight: 800, color: '#14532d', marginTop: 2 }}>{stat.value}</div>
                </div>
              ))}
            </div>
          )}
        </div>
      ) : (
        /* No crop yet — prompt user */
        <div className="agri-card" style={{
          background: 'linear-gradient(135deg, #fef3c7 0%, #fef9c3 100%)',
          border: '2px dashed #fde047', borderRadius: 24, padding: 28,
          textAlign: 'center'
        }}>
          <div style={{ fontSize: 52, marginBottom: 12 }}>🌾</div>
          <h3 style={{ fontSize: 20, fontWeight: 800, color: '#92400e', marginBottom: 6 }}>
            Ready for your first crop prediction?
          </h3>
          <p style={{ fontSize: 14, color: '#78350f', marginBottom: 18, maxWidth: 480, margin: '0 auto 18px' }}>
            First complete your soil test in <strong>Soil Test</strong> tab, then click <strong>Get Crop Recommendation</strong> to see AI-powered results with alternatives.
          </p>
          <div style={{ display: 'flex', gap: 12, justifyContent: 'center', flexWrap: 'wrap' }}>
            <button id="btn-goto-soil" onClick={() => setCurrentTab('sensors')} className="btn btn-primary">
              <Cpu size={16} /> Start Soil Test First
            </button>
            <button id="btn-goto-crop" onClick={() => setCurrentTab('crop')} className="btn btn-secondary">
              <Wheat size={16} /> I'll Enter Values Manually
            </button>
          </div>
        </div>
      )}

      {/* ══════════════════════════════════════════════
          ALL FEATURES GRID
          ══════════════════════════════════════════════ */}
      <div>
        <div className="section-title">
          <Layers size={20} color="#15803d" />
          {t.dashboard?.quickActions || 'All Farm Features'}
        </div>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(260px, 1fr))', gap: 16 }}>
          {featureGrid.map((f) => (
            <div
              key={f.id}
              id={`feature-${f.id}`}
              className={`feature-card ${f.color}`}
              onClick={() => setCurrentTab(f.id)}
              role="button"
              tabIndex={0}
              onKeyDown={(e) => e.key === 'Enter' && setCurrentTab(f.id)}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                <div className="feature-icon" style={{ background: f.iconBg, color: f.iconColor, fontSize: 22 }}>
                  {f.icon}
                </div>
                <ChevronRight size={16} color="#94a3b8" />
              </div>
              <div>
                <h4 style={{ fontSize: 15, fontWeight: 800, color: '#0f172a', marginBottom: 5 }}>{f.title}</h4>
                <p style={{ fontSize: 12.5, color: '#64748b', lineHeight: 1.5, margin: 0 }}>{f.desc}</p>
              </div>
              <button
                onClick={(e) => { e.stopPropagation(); setCurrentTab(f.id); }}
                className="btn btn-secondary"
                style={{ padding: '7px 14px', fontSize: 12, borderRadius: 10, alignSelf: 'flex-start' }}
              >
                {f.cta} →
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* ══════════════════════════════════════════════
          EMERGENCY HELPLINE FOOTER
          ══════════════════════════════════════════════ */}
      <div className="agri-card" style={{
        background: '#fef3c7', border: '2px solid #fde68a',
        borderRadius: 18, padding: '16px 22px',
        display: 'flex', justifyContent: 'space-between',
        alignItems: 'center', flexWrap: 'wrap', gap: 12
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: 26 }}>📞</span>
          <div>
            <div style={{ fontWeight: 800, fontSize: 14, color: '#92400e' }}>
              Kisan Call Centre (Toll-Free): 1551 / 1800-180-1551
            </div>
            <div style={{ fontSize: 12, color: '#78350f' }}>
              Agricultural scientists available 6 AM – 10 PM all 7 days
            </div>
          </div>
        </div>
        <a
          href="tel:1551"
          id="btn-kisan-call"
          className="btn"
          style={{ background: '#b45309', color: 'white', fontWeight: 800, fontSize: 13, padding: '8px 18px', borderRadius: 10, textDecoration: 'none' }}
        >
          Call 1551 📞
        </a>
      </div>
    </div>
  );
}
