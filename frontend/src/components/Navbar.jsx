import React, { useState } from 'react';
import {
  Sprout, Wifi, WifiOff, Languages, UserCheck, LogOut, Sparkles,
  LayoutDashboard, Wheat, Activity, Droplets, FlaskConical, Stethoscope,
  TrendingUp, Building2, Mic, MessageSquareCode, HelpCircle, Cpu, Server,
  Menu, X, Radio, ChevronDown
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
    { id: 'crop',       label: t.nav?.crop || 'Crop AI',              icon: Wheat,          },
    { id: 'soil',       label: t.nav?.soil || 'Soil Health',          icon: Activity },
    { id: 'irrigation', label: t.nav?.irrigation || 'Irrigation',     icon: Droplets },
    { id: 'fertilizer', label: t.nav?.fertilizer || 'Fertilizer',     icon: FlaskConical },
    { id: 'disease',    label: t.nav?.disease || 'Plant Doctor',      icon: Stethoscope },
    { id: 'mandi',      label: t.nav?.mandi || 'Mandi Prices',        icon: TrendingUp },
    { id: 'schemes',    label: t.nav?.schemes || 'Govt Schemes',      icon: Building2 },
    { id: 'voice',      label: t.nav?.voice || 'Voice AI',            icon: Mic,             },
    { id: 'chat',       label: t.nav?.chat || 'AI Chat',              icon: MessageSquareCode },
    { id: 'help',       label: t.nav?.help || 'Help Guide',           icon: HelpCircle },
  ];

  const languagesList = Object.keys(TRANSLATIONS);

  // Mobile bottom nav — 5 essential quick-access items
  const mobileItems = [
    { id: 'dashboard', label: t.nav?.dashboard || 'Home',      icon: LayoutDashboard },
    { id: 'crop',      label: t.nav?.crop || 'Crop AI',        icon: Wheat },
    { id: 'voice',     label: t.nav?.voice || 'Voice AI',      icon: Mic, highlight: true },
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
    <div style={{ position: 'fixed',margin: 0, top: 0, zIndex: 1000, width: '100%',height: 'auto', boxSizing: 'border-box' }}>
      {/* ── OFFICIAL GOVT OF INDIA TRICOLOR & MINISTRY BANNER ── */}
      <div className="govt-tricolor-bar" />
      <div className="govt-top-strip">
        <div style={{ display: 'flex', alignItems: 'center', gap: 7 ,paddingLeft: 12, paddingRight: 12,paddingTop: 2, paddingBottom: 2,  fontSize: 11, fontWeight: 700 }}>
          <span style={{ fontSize: 12 }}>🇮🇳</span>
          <span>भारत सरकार | कृषि एवं किसान कल्याण मंत्रालय (Ministry of Agriculture & Farmers Welfare)</span>
        </div>
        <div className="govt-top-strip-right hide-on-mobile" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span>डिजिटल कृषि मिशन</span>
          <span style={{ color: '#86efac' }}>•</span>
          <span style={{ color: '#fef08a', fontWeight: 800 }}>📞 किसान कॉल सेंटर: 1551 (Toll-Free 24×7)</span>
        </div>
      </div>

      {/* ── TOP BAR ── */}
      <header className="navbar" style={{
        background: 'rgba(255, 255, 255, 0.96)',
        backdropFilter: 'blur(20px) saturate(180%)',
        borderBottom: '1px solid rgba(21, 128, 61, 0.18)',
        boxShadow: '0 2px 14px rgba(0, 0, 0, 0.04)'
      }}>
        <div className="navbar-top" style={{ padding: '8px 14px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          
          {/* ── TOP-LEFT CONTROLS: MENU BUTTON + FARMER PROFILE + BRAND ── */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, minWidth: 0 }}>
            {/* Top-Left Menu Drawer Button */}
            <button
              id="btn-top-menu"
              onClick={() => setMobileDrawerOpen(!mobileDrawerOpen)}
              className="btn"
              style={{
                padding: '6px 12px',
                height: 38,
                borderRadius: 12,
                background: mobileDrawerOpen ? '#0f5132' : '#f0fdf4',
                color: mobileDrawerOpen ? '#ffffff' : '#0f5132',
                border: '1.5px solid #86efac',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                fontWeight: 800,
                fontSize: 13,
                cursor: 'pointer',
                boxShadow: '0 2px 6px rgba(15, 81, 50, 0.08)',
                flexShrink: 0
              }}
              aria-label="Open all modules menu"
              title="All Modules & Tools"
            >
              {mobileDrawerOpen ? <X size={18} /> : <Menu size={18} />}
              <span style={{ fontWeight: 800 }}>{'Modules'}</span>
            </button>

            

            {/* Portal Brand Emblem */}
            <div
              className="nav-brand hide-on-tiny"
              onClick={() => { setCurrentTab('dashboard'); setMobileDrawerOpen(false); }}
              style={{ display: 'flex', alignItems: 'center', gap: 7, cursor: 'pointer', minWidth: 0 }}
            >
              <div style={{
                width: 36,
                height: 36,
                borderRadius: 10,
                background: 'linear-gradient(135deg, #0f5132 0%, #15803d 100%)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                color: 'white',
                flexShrink: 0,
                boxShadow: '0 2px 8px rgba(15, 81, 50, 0.25)'
              }}>
                <Sprout size={20} />
              </div>
              <div className="" style={{ minWidth: 0 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                  <span style={{
                    fontSize: 14,
                    fontWeight: 900,
                    color: '#0f172a',
                    letterSpacing: '-0.3px',
                    fontFamily: 'Outfit, sans-serif',
                    whiteSpace: 'nowrap'
                  }}>
                    {'AgriSense AI'}
                  </span>
                  <span style={{
                    fontSize: 8.5,
                    fontWeight: 900,
                    padding: '2px 5px',
                    borderRadius: 99,
                    background: '#0f5132',
                    color: '#ffffff'
                  }}>
                    GOVT
                  </span>
                </div>
                <div style={{ fontSize: 10, color: '#15803d', fontWeight: 700, whiteSpace: 'nowrap' }}>
                  రాష్ట్రీయ కిసాన్ పోర్టల్
                </div>
              </div>
            </div>
          </div>

          {/* ── TOP-RIGHT CONTROLS: STATUS + LANGUAGE + LOGOUT ── */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, flexShrink: 0 }}>
            

            {/* IoT Telemetry status (Desktop only) */}
            <div
              className={`badge ${sensorOnline ? 'badge-green' : 'badge-amber'} hide-on-mobile`}
              title={sensorOnline ? '7-in-1 Soil Sensor Online' : 'Manual Telemetry Mode'}
              style={{
                cursor: 'pointer',
                fontSize: 11,
                padding: '4px 9px',
                borderRadius: 99,
                fontWeight: 800,
                alignItems: 'center',
                gap: 5
              }}
              onClick={() => setCurrentTab('sensors')}
            >
              {sensorOnline ? <Wifi size={12} className="pulse-glow" /> : <WifiOff size={12} />}
              <span>{sensorOnline ? 'IoT Live' : 'Manual'}</span>
            </div>

            {/* Language Selector Dropdown (High-Contrast & Touch Friendly) */}
            <div  style={{
              display: 'flex',
              alignItems: 'center',
              background: '#f8fafc',
              borderRadius: 14,
              padding: '4px 8px',
              gap: 5,
              border: '1.5px solid #cbd5e1',
              boxShadow: '0 1px 3px rgba(0,0,0,0.04)',
              height: 38,
              boxSizing: 'border-box'
            }}>
              <Languages size={15} style={{ color: '#15803d', flexShrink: 0 }} />
              <select
                aria-label="Select Language"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                style={{
                  border: 'none',
                  background: 'transparent',
                  fontWeight: 800,
                  fontSize: 13,
                  color: '#0f172a',
                  outline: 'none',
                  cursor: 'pointer',
                  maxWidth: 95
                }}
              >
                {languagesList.map((lang) => (
                  <option key={lang} value={lang}>{lang}</option>
                ))}
              </select>
            </div>

            {/* Farmer Logout Button (Desktop) */}
            {farmer && (
              <button
                onClick={onLogout}
                className="btn btn-secondary hide-on-mobile"
                style={{ padding: '6px 10px',width: 58,background: 'red',color: 'white', border: '1.5px solid #cbd5e1', height: 38, fontSize: 12, borderRadius: 12 }}
                title="Logout"
              >
                <LogOut size={19} />
              </button>
            )}
          </div>
        </div>

        {/* ── SCROLLABLE NAV TABS (DESKTOP / TABLET) ── */}
        <div className="navbar-bottom" style={{
          background: 'rgba(248, 250, 252, 0.85)',
          borderTop: '1px solid rgba(226, 232, 240, 0.8)'
        }}>
          <nav className="nav-tabs" style={{ padding: '8px 12px' }}>
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
                  style={{
                    borderRadius: 12,
                    padding: '8px 15px',
                    fontSize: 13,
                    fontWeight: 800,
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 7
                  }}
                >
                  <Icon size={15} />
                  <span>{item.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </header>

      {/* ── MOBILE FULL DRAWER MODAL ── */}
      {mobileDrawerOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 999,
            background: 'rgba(15, 23, 42, 0.65)',
            backdropFilter: 'blur(8px)',
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
              borderTopLeftRadius: 28,
              borderTopRightRadius: 28,
              padding: '24px 20px 96px 20px',
              maxHeight: '85vh',
              overflowY: 'auto',
              boxShadow: '0 -10px 40px rgba(0,0,0,0.25)',
              borderTop: '2px solid #22c55e'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            {/* Drawer Header */}
            <div style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              marginBottom: 18,
              paddingBottom: 12,
              borderBottom: '1px solid #e2e8f0'
            }}>
              <div>
                <div style={{ fontSize: 17, fontWeight: 900, color: '#0f172a', fontFamily: 'Outfit, sans-serif' }}>
                  {t.appName || 'AgriSense AI'}
                </div>
                <div style={{ fontSize: 12, color: '#64748b' }}>
                  {farmer ? `👤 ${farmer.name}` : '🌱 Smart Agricultural Suite'}
                </div>
              </div>
              <button
                onClick={() => setMobileDrawerOpen(false)}
                style={{
                  background: '#f1f5f9',
                  border: 'none',
                  borderRadius: '50%',
                  width: 36,
                  height: 36,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  cursor: 'pointer',
                  color: '#64748b'
                }}
              >
                <X size={18} />
              </button>
            </div>

            {/* 12 Modules Grid in Drawer */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 130px), 1fr))', gap: 10 }}>
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
                      borderRadius: 16,
                      border: isActive ? '2px solid #15803d' : '1.5px solid #e2e8f0',
                      background: isActive ? '#f0fdf4' : '#ffffff',
                      color: isActive ? '#15803d' : '#1e293b',
                      fontSize: 13,
                      fontWeight: 800,
                      cursor: 'pointer',
                      textAlign: 'left',
                      boxShadow: '0 2px 6px rgba(0,0,0,0.03)'
                    }}
                  >
                    <div style={{
                      width: 34,
                      height: 34,
                      borderRadius: 10,
                      background: isActive ? '#15803d' : '#f1f5f9',
                      color: isActive ? '#ffffff' : '#15803d',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      flexShrink: 0
                    }}>
                      <Icon size={17} />
                    </div>
                    <span style={{ lineHeight: 1.25 }}>{item.label}</span>
                  </button>
                );
              })}
            </div>

            {/* Logout button inside drawer on mobile */}
            {farmer && (
              <div style={{ marginTop: 18, paddingTop: 14, borderTop: '1px solid #e2e8f0' }}>
                <button
                  onClick={() => {
                    onLogout();
                    setMobileDrawerOpen(false);
                  }}
                  className="btn btn-secondary"
                  style={{ width: '100%', height: 42, fontSize: 13, color: '#dc2626', borderColor: '#fca5a5' }}
                >
                  <LogOut size={15} />
                  <span>Logout of Profile ({farmer.name})</span>
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ── MOBILE BOTTOM NAV (5 ICONS DOCK) ── */}
      <nav className="mobile-nav" style={{
        background: 'rgba(255, 255, 255, 0.95)',
        backdropFilter: 'blur(20px) saturate(180%)',
        borderTop: '1px solid rgba(21, 128, 61, 0.18)',
        boxShadow: '0 -4px 20px rgba(0, 0, 0, 0.08)',
   
      }}>
        {mobileItems.map((item) => {
          const Icon = item.icon;
          const isActive = !item.isMenuToggle && currentTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => handleMobileNavClick(item)}
              className={`mobile-nav-item ${isActive ? 'active' : ''}`}
              style={{
                position: 'relative',
                padding: '6px 0',
                transition: 'all 0.15s ease'
              }}
            >
              {item.highlight && !isActive && (
                <span style={{
                  position: 'absolute',
                  top: 4,
                  right: '25%',
                  width: 7,
                  height: 7,
                  borderRadius: '50%',
                  background: '#22c55e'
                }} />
              )}
              <Icon size={21} style={{
                color: isActive ? '#15803d' : '#64748b',
                transform: isActive ? 'scale(1.1)' : 'scale(1)',
                transition: 'transform 0.15s ease'
              }} />
              <span style={{
                fontWeight: isActive ? 800 : 600,
                color: isActive ? '#15803d' : '#64748b',
                fontSize: 10.5
              }}>
                {item.label}
              </span>
            </button>
          );
        })}
      </nav>
    </div>
  );
}
