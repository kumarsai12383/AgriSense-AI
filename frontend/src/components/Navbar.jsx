import React, { useState } from 'react';
import {
  Sprout, Wifi, WifiOff, Languages, UserCheck, LogOut, Sparkles,
  LayoutDashboard, Wheat, Activity, Droplets, FlaskConical, Stethoscope,
  TrendingUp, Building2, Mic, MessageSquareCode, HelpCircle, Cpu, Server,
  Menu, X, Radio
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';

export default function Navbar({
  currentTab, setCurrentTab, language, setLanguage,
  farmer, onLogout, sensorOnline, serverOnline
}) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const [mobileDrawerOpen, setMobileDrawerOpen] = useState(false);

  const navItems = [
    { id: 'dashboard',  label: t.nav?.dashboard || 'Dashboard',      icon: LayoutDashboard },
    { id: 'sensors',    label: t.nav?.sensors || 'Soil Test',         icon: Cpu },
    { id: 'crop',       label: t.nav?.crop || 'Crop AI',              icon: Wheat,          highlight: true },
    { id: 'soil',       label: t.nav?.soil || 'Soil Health',          icon: Activity },
    { id: 'irrigation', label: t.nav?.irrigation || 'Irrigation',     icon: Droplets },
    { id: 'fertilizer', label: t.nav?.fertilizer || 'Fertilizer',     icon: FlaskConical },
    { id: 'disease',    label: t.nav?.disease || 'Plant Doctor',      icon: Stethoscope },
    { id: 'mandi',      label: t.nav?.mandi || 'Mandi Prices',        icon: TrendingUp },
    { id: 'schemes',    label: t.nav?.schemes || 'Govt Schemes',      icon: Building2 },
    { id: 'voice',      label: t.nav?.voice || 'Voice AI',            icon: Mic,            highlight: true },
    { id: 'chat',       label: t.nav?.chat || 'AI Chat',              icon: MessageSquareCode },
    { id: 'help',       label: t.nav?.help || 'Help Guide',           icon: HelpCircle },
  ];

  const languagesList = Object.keys(TRANSLATIONS);

  // Mobile bottom nav — 5 essential quick-access items
  const mobileItems = [
    { id: 'dashboard', label: t.nav?.dashboard || 'Home',      icon: LayoutDashboard },
    { id: 'crop',      label: t.nav?.crop || 'Crop AI',        icon: Wheat },
    { id: 'voice',     label: t.nav?.voice || 'Voice AI',      icon: Mic },
    { id: 'mandi',     label: t.nav?.mandi || 'Mandi',         icon: TrendingUp },
    { id: 'menu',      label: t.nav?.menu || 'Menu',           icon: Menu, isMenuToggle: true },
  ];

  const handleMobileNavClick = (item) => {
    if (item.isMenuToggle) {
      setMobileDrawerOpen(!mobileDrawerOpen);
    } else {
      setCurrentTab(item.id);
      setMobileDrawerOpen(false);
    }
  };

  return (
    <>
      {/* ── TOP BAR ── */}
      <header className="navbar">
        <div className="navbar-top">
          {/* Brand */}
          <div className="nav-brand" onClick={() => setCurrentTab('dashboard')}>
            <div className="brand-icon">
              <Sprout size={24} />
            </div>
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <span style={{ fontSize: 18, fontWeight: 800, color: '#0f172a', letterSpacing: '-0.5px', fontFamily: 'Outfit, sans-serif' }}>
                  {t.appName || 'AgriSense AI'}
                </span>
                <span className="badge badge-green" style={{ fontSize: 9, padding: '2px 7px', letterSpacing: '0.5px' }}>
                  PRO
                </span>
              </div>
              <div className="hide-on-mobile" style={{ fontSize: 10.5, color: '#64748b', fontWeight: 600 }}>
                {t.tagline || 'Smart Agricultural Intelligence'}
              </div>
            </div>
          </div>

          {/* Right Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            {/* Server status (dot on small mobile) */}
            <div
              className={`badge ${serverOnline ? 'badge-green' : 'badge-amber'}`}
              title={serverOnline ? 'Backend API online' : 'Backend API offline'}
              style={{ cursor: 'default', fontSize: 11, padding: '4px 8px' }}
            >
              <Server size={11} />
              <span className="hide-on-small-mobile">{serverOnline ? 'API Live' : 'API Off'}</span>
            </div>

            {/* IoT Sensor status */}
            <div
              className={`badge ${sensorOnline ? 'badge-green' : 'badge-amber'}`}
              title={sensorOnline ? 'ESP32 sensor transmitting' : 'No IoT packet in last 10 min'}
              style={{ cursor: 'pointer', fontSize: 11, padding: '4px 8px' }}
              onClick={() => setCurrentTab('sensors')}
            >
              {sensorOnline
                ? <Wifi size={11} className="pulse-glow" />
                : <WifiOff size={11} />}
              <span className="hide-on-small-mobile">{sensorOnline ? 'IoT Live' : 'IoT Off'}</span>
            </div>

            {/* Language selector (High-Contrast & Touch Friendly) */}
            <div style={{
              display: 'flex', alignItems: 'center',
              background: '#f1f5f9', borderRadius: 12, padding: '4px 8px', gap: 4,
              border: '1px solid #e2e8f0'
            }}>
              <Languages size={15} style={{ color: '#15803d', flexShrink: 0 }} />
              <select
                aria-label="Select Language"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{
                  border: 'none', background: 'transparent',
                  fontWeight: 800, fontSize: 12.5, color: '#0f172a',
                  outline: 'none', cursor: 'pointer', maxWidth: 96
                }}
              >
                {languagesList.map((lang) => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>

            {/* Farmer profile (Desktop / Tablet) */}
            {farmer && (
              <div className="hide-on-mobile" style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                <div style={{
                  display: 'flex', alignItems: 'center', gap: 6,
                  background: '#f8fafc', border: '1.5px solid #e2e8f0',
                  padding: '5px 11px', borderRadius: 10, maxWidth: 130
                }}>
                  <UserCheck size={14} style={{ color: '#15803d', flexShrink: 0 }} />
                  <span style={{
                    fontSize: 12.5, fontWeight: 700, color: '#0f172a',
                    overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'
                  }}>
                    {farmer.name}
                  </span>
                </div>
                <button
                  onClick={onLogout}
                  className="btn btn-secondary"
                  style={{ padding: '6px 10px', height: 34, fontSize: 12 }}
                  title="Logout"
                >
                  <LogOut size={13} />
                </button>
              </div>
            )}

            {/* Mobile Hamburger Drawer Button */}
            <button
              onClick={() => setMobileDrawerOpen(!mobileDrawerOpen)}
              className="btn btn-secondary show-on-mobile"
              style={{ padding: '6px 10px', height: 34 }}
              aria-label="Open menu"
            >
              {mobileDrawerOpen ? <X size={16} /> : <Menu size={16} />}
            </button>
          </div>
        </div>

        {/* ── SCROLLABLE NAV TABS (DESKTOP / TABLET) ── */}
        <div className="navbar-bottom">
          <nav className="nav-tabs">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  id={`nav-${item.id}`}
                  onClick={() => {
                    setCurrentTab(item.id);
                    setMobileDrawerOpen(false);
                  }}
                  className={`nav-tab ${isActive ? 'active' : ''} ${item.highlight && !isActive ? 'highlight' : ''}`}
                >
                  <Icon size={14} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* ── MOBILE FULL-MENU DRAWER (SLIDE-UP / OVERLAY) ── */}
      {mobileDrawerOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 1000,
            background: 'rgba(0, 0, 0, 0.55)',
            backdropFilter: 'blur(6px)',
            display: 'flex',
            flexDirection: 'column',
            justifyContent: 'flex-end',
            animation: 'fadeIn 0.2s ease-out'
          }}
          onClick={() => setMobileDrawerOpen(false)}
        >
          <div
            style={{
              background: '#ffffff',
              borderTopLeftRadius: 26,
              borderTopRightRadius: 26,
              padding: '20px 20px 80px 20px',
              maxHeight: '80vh',
              overflowY: 'auto',
              boxShadow: '0 -10px 40px rgba(0,0,0,0.25)'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Drawer Header */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16, borderBottom: '1px solid #f1f5f9', paddingBottom: 12 }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                <Sprout size={20} color="#15803d" />
                <span style={{ fontSize: 16, fontWeight: 800, color: '#0f172a' }}>
                  {t.nav?.menu || "All AgriSense Services"}
                </span>
              </div>
              <button
                onClick={() => setMobileDrawerOpen(false)}
                style={{ background: '#f1f5f9', border: 'none', borderRadius: 99, padding: 6, cursor: 'pointer' }}
              >
                <X size={18} color="#475569" />
              </button>
            </div>

            {/* Farmer Profile Strip in Drawer */}
            {farmer && (
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', background: '#f0fdf4', padding: '10px 14px', borderRadius: 14, marginBottom: 16, border: '1px solid #bbf7d0' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <UserCheck size={18} color="#15803d" />
                  <div>
                    <div style={{ fontSize: 13.5, fontWeight: 800, color: '#0f172a' }}>{farmer.name}</div>
                    <div style={{ fontSize: 11, color: '#166534' }}>{farmer.phone || 'Farmer Profile'} • {language}</div>
                  </div>
                </div>
                <button
                  onClick={onLogout}
                  className="btn btn-secondary"
                  style={{ padding: '6px 12px', fontSize: 11, color: '#b91c1c' }}
                >
                  <LogOut size={12} />
                  <span>Logout</span>
                </button>
              </div>
            )}

            {/* 12 Modules Grid in Drawer */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: 10 }}>
              {navItems.map((item) => {
                const Icon = item.icon;
                const isActive = currentTab === item.id;
                return (
                  <button
                    key={item.id}
                    onClick={() => {
                      setCurrentTab(item.id);
                      setMobileDrawerOpen(false);
                    }}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: 10,
                      padding: '12px 14px',
                      borderRadius: 14,
                      border: isActive ? '2px solid #15803d' : '1px solid #e2e8f0',
                      background: isActive ? '#f0fdf4' : '#ffffff',
                      color: isActive ? '#15803d' : '#1e293b',
                      fontSize: 13,
                      fontWeight: 700,
                      cursor: 'pointer',
                      textAlign: 'left',
                      boxShadow: '0 2px 4px rgba(0,0,0,0.02)'
                    }}
                  >
                    <div style={{
                      width: 32, height: 32, borderRadius: 10,
                      background: isActive ? '#15803d' : '#f1f5f9',
                      color: isActive ? '#ffffff' : '#15803d',
                      display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0
                    }}>
                      <Icon size={16} />
                    </div>
                    <span style={{ lineHeight: 1.3 }}>{item.label}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* ── MOBILE BOTTOM NAV (5 ICONS DOCK) ── */}
      <nav className="mobile-nav">
        {mobileItems.map((item) => {
          const Icon = item.icon;
          const isActive = !item.isMenuToggle && currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => handleMobileNavClick(item)}
              className={`mobile-nav-item ${isActive ? 'active' : ''}`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>
    </>
  );
}
