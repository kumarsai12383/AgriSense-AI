import React, { useState } from 'react';
import { Sprout, Phone, User, ArrowRight, ShieldCheck, Cpu, Droplets, Wheat } from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

export default function LoginModal({ language, setLanguage, onLoginSuccess, addToast }) {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!name.trim()) {
      addToast('Please enter your farmer name', 'error');
      return;
    }
    const cleanPhone = phone.replace(/\D/g, '');
    if (cleanPhone.length !== 10) {
      addToast('Please enter a valid 10-digit mobile number', 'error');
      return;
    }

    setLoading(true);
    try {
      const res = await api.loginFarmer(name.trim(), cleanPhone, language);
      if (res && res.farmer) {
        onLoginSuccess(res.farmer);
        addToast(`Namaste ${res.farmer.name}! Welcome to AgriSense AI`, 'success');
      }
    } catch (err) {
      console.error('Login error:', err);
      // Fallback offline mock farmer profile if backend is starting
      const mockFarmer = { id: 1, name: name.trim(), phone: cleanPhone, language };
      onLoginSuccess(mockFarmer);
      addToast(`Logged in as ${mockFarmer.name}`, 'info');
    } finally {
      setLoading(false);
    }
  };

  const pillars = [
    { title: "🌾 ML Crop Science", desc: "Predicts the highest-yielding crop tailored to your exact NPK & weather.", icon: Wheat },
    { title: "💧 Smart Irrigation", desc: "Automated root zone moisture alerts and water budgeting.", icon: Droplets },
    { title: "🧪 7-in-1 Soil Testing", desc: "Instant N-P-K nutrient diagnostics, pH check, and fertilizer dosing.", icon: Cpu },
    { title: "🎙️ Multilingual Voice AI", desc: "Real-time speech interaction in 6 Indian languages with Gemini Live.", icon: Sprout },
  ];

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'rgba(15, 23, 42, 0.75)',
      backdropFilter: 'blur(8px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: 16
    }}>
      <div 
        className="agri-card"
        style={{
          width: '100%',
          maxWidth: 580,
          maxHeight: '92vh',
          overflowY: 'auto',
          padding: 32,
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.35)'
        }}
      >
        {/* Header Hero */}
        <div style={{
          background: 'linear-gradient(135deg, #14532d 0%, #16a34a 100%)',
          borderRadius: 18,
          padding: '24px 20px',
          color: 'white',
          textAlign: 'center',
          marginBottom: 24,
          position: 'relative',
          boxShadow: '0 8px 20px rgba(22, 163, 74, 0.25)'
        }}>
          <div style={{
            width: 56,
            height: 56,
            background: 'rgba(255, 255, 255, 0.2)',
            borderRadius: '50%',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 10px auto',
            fontSize: 30
          }}>
            🌱
          </div>
          <h2 style={{ color: 'white', fontSize: 24, margin: '0 0 6px 0' }}>
            {t.appName}
          </h2>
          <p style={{ color: '#dcfce7', fontSize: 13, margin: 0, fontWeight: 600 }}>
            {t.tagline}
          </p>

          {/* Language Switcher Buttons */}
          <div style={{
            display: 'flex',
            gap: 6,
            justifyContent: 'center',
            flexWrap: 'wrap',
            marginTop: 14
          }}>
            {Object.keys(TRANSLATIONS).map((lang) => (
              <button
                key={lang}
                type="button"
                onClick={() => setLanguage(lang)}
                style={{
                  background: language === lang ? '#ffffff' : 'rgba(255, 255, 255, 0.2)',
                  color: language === lang ? '#14532d' : '#ffffff',
                  border: 'none',
                  borderRadius: 20,
                  padding: '4px 12px',
                  fontSize: 12,
                  fontWeight: 700,
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
              >
                {lang}
              </button>
            ))}
          </div>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit}>
          <div style={{ marginBottom: 18 }}>
            <div style={{ fontSize: 16, fontWeight: 800, color: '#0f172a', marginBottom: 4 }}>
              {t.login.title}
            </div>
            <div style={{ fontSize: 13, color: '#64748b' }}>
              {t.login.subtitle}
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <User size={15} style={{ color: '#15803d' }} />
                {t.login.name}
              </span>
            </label>
            <input
              type="text"
              className="input-field"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder={t.login.placeholderName}
              required
            />
          </div>

          <div className="input-group">
            <label className="input-label">
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Phone size={15} style={{ color: '#15803d' }} />
                {t.login.phone}
              </span>
            </label>
            <input
              type="tel"
              maxLength={10}
              className="input-field"
              value={phone}
              onChange={(e) => setPhone(e.target.value.replace(/\D/g, ''))}
              placeholder={t.login.placeholderPhone}
              required
            />
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{ width: '100%', height: 48, marginTop: 10, fontSize: 16 }}
          >
            {loading ? (
              <span>Authenticating...</span>
            ) : (
              <>
                <span>{t.login.submit}</span>
                <ArrowRight size={18} />
              </>
            )}
          </button>
        </form>

        {/* 4 Pillars Info Grid */}
        <div style={{ marginTop: 24, paddingTop: 18, borderTop: '1px solid #e2e8f0' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 10 }}>
            {pillars.map((p, idx) => {
              const Icon = p.icon;
              return (
                <div 
                  key={idx} 
                  style={{
                    background: '#f8fafc',
                    padding: '10px 12px',
                    borderRadius: 12,
                    border: '1px solid #e2e8f0'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, fontWeight: 700, color: '#15803d', marginBottom: 2 }}>
                    <Icon size={14} />
                    <span>{p.title}</span>
                  </div>
                  <div style={{ fontSize: 11, color: '#64748b', lineHeight: 1.3 }}>
                    {p.desc}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
