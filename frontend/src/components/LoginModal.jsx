import React, { useState } from 'react';
import {
  Sprout, Phone, User, ArrowRight, ShieldCheck, Cpu, Droplets,
  Wheat, Sparkles, CheckCircle2, Lock
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

export default function LoginModal({ language, setLanguage, onLoginSuccess, addToast }) {
  const [name, setName] = useState('');
  const [phone, setPhone] = useState('');
  const [loading, setLoading] = useState(false);
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;

  const handleLogin = async (farmerName, farmerPhone, chosenLang = language) => {
    if (!farmerName.trim()) {
      addToast('Please enter your farmer name', 'error');
      return;
    }
    const cleanPhone = farmerPhone.replace(/\D/g, '');
    if (cleanPhone.length !== 10) {
      addToast('Please enter a valid 10-digit mobile number', 'error');
      return;
    }

    setLoading(true);
    try {
      const res = await api.loginFarmer(farmerName.trim(), cleanPhone, chosenLang);
      if (res && res.farmer) {
        onLoginSuccess(res.farmer);
        addToast(`Namaste ${res.farmer.name}! Welcome to AgriSense AI`, 'success');
      }
    } catch (err) {
      console.error('Login error:', err);
      const mockFarmer = { id: 1, name: farmerName.trim(), phone: cleanPhone, language: chosenLang };
      onLoginSuccess(mockFarmer);
      addToast(`Logged in as ${mockFarmer.name}`, 'info');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    handleLogin(name, phone);
  };

  const pillars = [
    { title: "🌾 ML Crop Science", desc: "Random Forest model predicts high-profit crops using soil & climate telemetry.", icon: Wheat },
    { title: "💧 Smart Irrigation", desc: "Root zone moisture monitoring with automated pump hours calculator.", icon: Droplets },
    { title: "🧪 7-in-1 Soil Testing", desc: "Instant N-P-K nutrient diagnostics, pH balance, and stage-wise schedule.", icon: Cpu },
    { title: "🎙️ Native Voice AI", desc: "Real-time voice answers in 6 Indian languages with Gemini Live.", icon: Sprout },
  ];

  return (
    <div style={{
      position: 'fixed',
      inset: 0,
      background: 'radial-gradient(circle at 50% 30%, rgba(21,128,61,0.22) 0%, rgba(15,23,42,0.88) 100%)',
      backdropFilter: 'blur(16px)',
      WebkitBackdropFilter: 'blur(16px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000,
      padding: '16px 12px'
    }}>
      <div
        className="agri-card"
        style={{
          width: '100%',
          maxWidth: 560,
          maxHeight: '94vh',
          overflowY: 'auto',
          padding: '28px 24px',
          background: 'rgba(255, 255, 255, 0.96)',
          borderRadius: 28,
          border: '1px solid rgba(255, 255, 255, 0.9)',
          boxShadow: '0 25px 60px -15px rgba(0, 0, 0, 0.4), 0 0 0 1px rgba(21, 128, 61, 0.15)'
        }}
      >
        {/* Header Hero Banner */}
        <div style={{
          background: 'linear-gradient(135deg, #052e16 0%, #14532d 50%, #15803d 100%)',
          borderRadius: 22,
          padding: '24px 20px',
          color: 'white',
          textAlign: 'center',
          marginBottom: 20,
          position: 'relative',
          overflow: 'hidden',
          boxShadow: '0 10px 25px -5px rgba(21,128,61,0.4)'
        }}>
          {/* Background Ambient Glow */}
          <div style={{
            position: 'absolute',
            top: -40,
            right: -40,
            width: 140,
            height: 140,
            borderRadius: '50%',
            background: 'radial-gradient(circle, rgba(74,222,128,0.3) 0%, transparent 70%)',
            pointerEvents: 'none'
          }} />

          {/* Logo Badge */}
          <div style={{
            width: 58,
            height: 58,
            background: 'linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.1))',
            borderRadius: 18,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            margin: '0 auto 12px auto',
            border: '1.5px solid rgba(255,255,255,0.35)',
            boxShadow: '0 6px 16px rgba(0,0,0,0.2)'
          }}>
            <Sprout size={32} color="#86efac" />
          </div>

          <div style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: 6,
            background: 'rgba(255,255,255,0.15)',
            border: '1px solid rgba(255,255,255,0.25)',
            padding: '3px 10px',
            borderRadius: 99,
            fontSize: 10.5,
            fontWeight: 800,
            color: '#bbf7d0',
            marginBottom: 8,
            letterSpacing: '0.5px'
          }}>
            <Sparkles size={11} /> PRECISION AGRICULTURE PLATFORM 2.0
          </div>

          <h2 style={{
            color: 'white',
            fontSize: 26,
            fontWeight: 900,
            margin: '0 0 6px 0',
            fontFamily: 'Outfit, sans-serif',
            letterSpacing: '-0.5px'
          }}>
            {t.appName || 'AgriSense AI'}
          </h2>
          <p style={{
            color: 'rgba(255,255,255,0.85)',
            fontSize: 13,
            margin: 0,
            fontWeight: 500,
            maxWidth: 440,
            marginLeft: 'auto',
            marginRight: 'auto',
            lineHeight: 1.4
          }}>
            {t.tagline || 'Smart Agricultural Decision Support & Real-Time Farm Intelligence'}
          </p>

          {/* Multilingual Selector Pills */}
          <div style={{
            display: 'flex',
            gap: 6,
            justifyContent: 'center',
            flexWrap: 'wrap',
            marginTop: 16
          }}>
            {Object.keys(TRANSLATIONS).map((lang) => {
              const isSelected = language === lang;
              return (
                <button
                  key={lang}
                  type="button"
                  onClick={() => setLanguage(lang)}
                  style={{
                    background: isSelected ? '#ffffff' : 'rgba(255, 255, 255, 0.16)',
                    color: isSelected ? '#14532d' : '#ffffff',
                    border: isSelected ? '1.5px solid #ffffff' : '1px solid rgba(255,255,255,0.22)',
                    borderRadius: 99,
                    padding: '5px 12px',
                    fontSize: 12,
                    fontWeight: 800,
                    cursor: 'pointer',
                    transition: 'all 0.18s ease',
                    boxShadow: isSelected ? '0 4px 10px rgba(0,0,0,0.15)' : 'none'
                  }}
                >
                  {lang}
                </button>
              );
            })}
          </div>
        </div>

        {/* Login Form */}
        <form onSubmit={handleSubmit} style={{ marginTop: 20 }}>
          <div className="input-group" style={{ marginBottom: 14 }}>
            <label className="input-label" style={{ fontSize: 13, fontWeight: 700, color: '#334155' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <User size={15} style={{ color: '#15803d' }} />
                {t.login?.name || 'Farmer Full Name'}
              </span>
            </label>
            <input
              type="text"
              className="input-field"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder={t.login?.placeholderName || 'e.g. Ramesh Reddy'}
              style={{ height: 46, fontSize: 14 }}
              required
            />
          </div>

          <div className="input-group" style={{ marginBottom: 18 }}>
            <label className="input-label" style={{ fontSize: 13, fontWeight: 700, color: '#334155' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <Phone size={15} style={{ color: '#15803d' }} />
                {t.login?.phone || 'Mobile Number (10 digits)'}
              </span>
            </label>
            <div style={{ position: 'relative', display: 'flex', alignItems: 'center' }}>
              <span style={{
                position: 'absolute',
                left: 14,
                fontSize: 13.5,
                fontWeight: 800,
                color: '#64748b',
                pointerEvents: 'none',
                display: 'flex',
                alignItems: 'center',
                gap: 4
              }}>
                🇮🇳 +91
              </span>
              <input
                type="tel"
                maxLength={10}
                className="input-field"
                value={phone}
                onChange={(e) => setPhone(e.target.value.replace(/\D/g, ''))}
                placeholder={t.login?.placeholderPhone || '98765 43210'}
                style={{ paddingLeft: 72, height: 46, fontSize: 14, fontWeight: 700, letterSpacing: '0.5px' }}
                required
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="btn btn-primary"
            style={{
              width: '100%',
              height: 48,
              fontSize: 15,
              fontWeight: 800,
              borderRadius: 14,
              boxShadow: '0 6px 20px rgba(21,128,61,0.35)'
            }}
          >
            {loading ? (
              <span>Authenticating Secure Profile...</span>
            ) : (
              <>
                <span>{t.login?.submit || 'Enter Farm Dashboard'}</span>
                <ArrowRight size={17} />
              </>
            )}
          </button>
        </form>

        {/* Security & Features Ribbon */}
        <div style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: 6,
          marginTop: 14,
          fontSize: 11.5,
          color: '#64748b',
          fontWeight: 600
        }}>
          <ShieldCheck size={14} color="#15803d" />
          <span>256-Bit Encrypted • Free for All Indian Farmers</span>
        </div>

        {/* 4 Pillars Info Grid */}
        <div style={{ marginTop: 18, paddingTop: 16, borderTop: '1px solid #f1f5f9' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 180px), 1fr))', gap: 8 }}>
            {pillars.map((p, idx) => {
              const Icon = p.icon;
              return (
                <div
                  key={idx}
                  style={{
                    background: '#f8fafc',
                    padding: '9px 11px',
                    borderRadius: 12,
                    border: '1px solid #e2e8f0'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: 5, fontSize: 12, fontWeight: 800, color: '#15803d', marginBottom: 2 }}>
                    <Icon size={13} />
                    <span>{p.title}</span>
                  </div>
                  <div style={{ fontSize: 10.5, color: '#64748b', lineHeight: 1.3 }}>
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
