import React from 'react';
import {
  Sprout, Wifi, WifiOff, Languages, UserCheck, LogOut, Sparkles,
  LayoutDashboard, Wheat, Activity, Droplets, FlaskConical, Stethoscope,
  TrendingUp, Building2, Mic, MessageSquareCode, HelpCircle, Cpu, Server
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';

export default function Navbar({
  currentTab, setCurrentTab, language, setLanguage,
  farmer, onLogout, sensorOnline, serverOnline
}) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;

  const navItems = [
    { id: 'dashboard',  label: t.nav.dashboard || 'Dashboard',      icon: LayoutDashboard },
    { id: 'sensors',    label: t.nav.sensors || 'Soil Test',         icon: Cpu },
    { id: 'crop',       label: t.nav.crop || 'Crop AI',              icon: Wheat,          highlight: true },
    { id: 'soil',       label: t.nav.soil || 'Soil Health',          icon: Activity },
    { id: 'irrigation', label: t.nav.irrigation || 'Irrigation',     icon: Droplets },
    { id: 'fertilizer', label: t.nav.fertilizer || 'Fertilizer',     icon: FlaskConical },
    { id: 'disease',    label: t.nav.disease || 'Plant Doctor',      icon: Stethoscope },
    { id: 'mandi',      label: t.nav.mandi || 'Mandi Prices',        icon: TrendingUp },
    { id: 'schemes',    label: t.nav.schemes || 'Govt Schemes',      icon: Building2 },
    { id: 'voice',      label: t.nav.voice || 'Voice AI',            icon: Mic,            highlight: true },
    { id: 'chat',       label: t.nav.chat || 'AI Chat',              icon: MessageSquareCode },
    { id: 'help',       label: t.nav.help || 'Help Guide',           icon: HelpCircle },
  ];

  const languagesList = Object.keys(TRANSLATIONS);

  // Mobile bottom nav — key 5 items
  const mobileItems = [
    { id: 'dashboard', label: 'Home',     icon: LayoutDashboard },
    { id: 'crop',      label: 'Crop AI',  icon: Wheat },
    { id: 'voice',     label: 'Voice',    icon: Mic },
    { id: 'mandi',     label: 'Mandi',    icon: TrendingUp },
    { id: 'schemes',   label: 'Schemes',  icon: Building2 },
  ];

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
              <div style={{ fontSize: 10.5, color: '#64748b', fontWeight: 600 }}>
                Smart Agricultural Intelligence
              </div>
            </div>
          </div>

          {/* Right Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            {/* Server status */}
            <div
              className={`badge ${serverOnline ? 'badge-green' : 'badge-amber'}`}
              title={serverOnline ? 'Backend API online' : 'Backend API offline'}
              style={{ cursor: 'default', fontSize: 10.5 }}
            >
              <Server size={11} />
              <span>{serverOnline ? 'API Live' : 'API Off'}</span>
            </div>

            {/* IoT Sensor status */}
            <div
              className={`badge ${sensorOnline ? 'badge-green' : 'badge-amber'}`}
              title={sensorOnline ? 'ESP32 sensor transmitting' : 'No IoT packet in last 10 min'}
              style={{ cursor: 'pointer' }}
              onClick={() => setCurrentTab('sensors')}
            >
              {sensorOnline
                ? <Wifi size={11} className="pulse-glow" />
                : <WifiOff size={11} />}
              <span>{sensorOnline ? 'IoT Live' : 'IoT Off'}</span>
            </div>

            {/* Language selector */}
            <div style={{
              display: 'flex', alignItems: 'center',
              background: '#f1f5f9', borderRadius: 10, padding: '5px 10px', gap: 5
            }}>
              <Languages size={14} style={{ color: '#15803d', flexShrink: 0 }} />
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{
                  border: 'none', background: 'transparent',
                  fontWeight: 700, fontSize: 12.5, color: '#0f172a',
                  outline: 'none', cursor: 'pointer', maxWidth: 90
                }}
              >
                {languagesList.map((lang) => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>

            {/* Farmer profile */}
            {farmer && (
              <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
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
          </div>
        </div>

        {/* ── SCROLLABLE NAV TABS ── */}
        <div className="navbar-bottom">
          <nav className="nav-tabs">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = currentTab === item.id;
              return (
                <button
                  key={item.id}
                  id={`nav-${item.id}`}
                  onClick={() => setCurrentTab(item.id)}
                  className={`nav-tab ${isActive ? 'active' : ''} ${item.highlight && !isActive ? 'highlight' : ''}`}
                >
                  <Icon size={13} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* ── MOBILE BOTTOM NAV ── */}
      <nav className="mobile-nav">
        {mobileItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => setCurrentTab(item.id)}
              className={`mobile-nav-item ${currentTab === item.id ? 'active' : ''}`}
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
