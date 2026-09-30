import React from 'react';
import { Activity, ShieldCheck, AlertCircle, CheckCircle, Info, Sparkles, Layers } from 'lucide-react';
import { TRANSLATIONS } from '../translations';

export default function SoilHealth({ farmData, language }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;

  const n = farmData?.nitrogen ?? 80;
  const p = farmData?.phosphorus ?? 40;
  const k = farmData?.potassium ?? 40;
  const ph = farmData?.ph ?? 6.5;

  // Status assessments
  const getNitrogenStatus = (val) => {
    if (val < 50) return { label: 'Low (Deficient)', color: '#dc2626', badge: 'badge-red', tip: 'Apply Farm Yard Manure (FYM) or split Urea dose.' };
    if (val > 140) return { label: 'High (Excess)', color: '#d97706', badge: 'badge-amber', tip: 'Avoid further nitrogenous fertilizer to prevent lodging.' };
    return { label: 'Optimal Range', color: '#15803d', badge: 'badge-green', tip: 'Maintain organic crop rotation.' };
  };

  const getPhStatus = (val) => {
    if (val < 6.0) return { label: 'Acidic Soil', color: '#dc2626', badge: 'badge-red', tip: 'Apply Agricultural Lime (Calcium Carbonate) or Wood Ash.' };
    if (val > 7.8) return { label: 'Alkaline / Saline', color: '#d97706', badge: 'badge-amber', tip: 'Apply Gypsum (Calcium Sulphate) and organic green manure (Dhaincha).' };
    return { label: 'Neutral (Optimal 6.5 - 7.5)', color: '#15803d', badge: 'badge-green', tip: 'Ideal for maximum macronutrient absorption.' };
  };

  const nStat = getNitrogenStatus(n);
  const phStat = getPhStatus(ph);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #1e3a8a 0%, #2563eb 100%)',
          color: 'white',
          padding: '24px 28px',
          borderRadius: 20
        }}
      >
        <h2 style={{ color: 'white', fontSize: 24, margin: '0 0 6px 0' }}>
          {t.soil.title}
        </h2>
        <p style={{ color: '#dbeafe', fontSize: 14, margin: 0, maxWidth: 650 }}>
          {t.soil.subtitle}
        </p>
      </div>

      {/* Grid: NPK Status Bars */}
      <div className="grid-2">
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <Activity size={20} style={{ color: '#2563eb' }} />
              <span>Primary Macronutrients (NPK) Balance</span>
            </div>
          </div>

          {/* Nitrogen Bar */}
          <div style={{ marginBottom: 18 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 6, marginBottom: 6 }}>
              <span style={{ fontSize: 13, fontWeight: 700, color: '#334155' }}>
                Nitrogen (N) — Vegetative Growth
              </span>
              <span className={`badge ${nStat.badge}`}>{n} kg/ha • {nStat.label}</span>
            </div>
            <div style={{ width: '100%', height: 10, background: '#e2e8f0', borderRadius: 99, overflow: 'hidden' }}>
              <div style={{ width: `${Math.min(100, (n / 160) * 100)}%`, height: '100%', background: nStat.color, borderRadius: 99 }} />
            </div>
            <div style={{ fontSize: 12, color: '#64748b', marginTop: 4 }}>{nStat.tip}</div>
          </div>

          {/* Phosphorus Bar */}
          <div style={{ marginBottom: 18 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 6, marginBottom: 6 }}>
              <span style={{ fontSize: 13, fontWeight: 700, color: '#334155' }}>
                Phosphorus (P) — Root Establishment
              </span>
              <span className="badge badge-green">{p} kg/ha • Optimal</span>
            </div>
            <div style={{ width: '100%', height: 10, background: '#e2e8f0', borderRadius: 99, overflow: 'hidden' }}>
              <div style={{ width: `${Math.min(100, (p / 100) * 100)}%`, height: '100%', background: '#15803d', borderRadius: 99 }} />
            </div>
            <div style={{ fontSize: 12, color: '#64748b', marginTop: 4 }}>Apply DAP or Single Super Phosphate (SSP) at root zone.</div>
          </div>

          {/* Potassium Bar */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 6, marginBottom: 6 }}>
              <span style={{ fontSize: 13, fontWeight: 700, color: '#334155' }}>
                Potassium (K) — Disease & Drought Resistance
              </span>
              <span className="badge badge-green">{k} kg/ha • Optimal</span>
            </div>
            <div style={{ width: '100%', height: 10, background: '#e2e8f0', borderRadius: 99, overflow: 'hidden' }}>
              <div style={{ width: `${Math.min(100, (k / 100) * 100)}%`, height: '100%', background: '#15803d', borderRadius: 99 }} />
            </div>
            <div style={{ fontSize: 12, color: '#64748b', marginTop: 4 }}>Apply Muriate of Potash (MOP) to boost grain test weight.</div>
          </div>
        </div>

        {/* Soil pH & Reaction */}
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <Layers size={20} style={{ color: '#854d0e' }} />
              <span>Soil pH Reaction & Chemical Environment</span>
            </div>
            <span className={`badge ${phStat.badge}`}>{phStat.label}</span>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 16, margin: '12px 0 20px 0' }}>
            <div style={{
              width: 76,
              height: 76,
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #d97706, #f59e0b)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'white',
              fontSize: 26,
              fontWeight: 800,
              boxShadow: '0 8px 18px rgba(217, 119, 6, 0.3)',
              flexShrink: 0
            }}>
              {ph}
            </div>
            <div style={{ minWidth: 0, flex: 1 }}>
              <div style={{ fontSize: 16, fontWeight: 800, color: '#0f172a' }}>
                {ph < 6.0 ? "Acidic Medium" : ph > 7.8 ? "Alkaline / Calcareous" : "Near-Neutral Sweet Zone"}
              </div>
              <div style={{ fontSize: 13, color: '#64748b', marginTop: 4 }}>
                {phStat.tip}
              </div>
            </div>
          </div>

          <div style={{ background: '#f8fafc', padding: 14, borderRadius: 14, border: '1px solid #e2e8f0' }}>
            <div style={{ fontSize: 13, fontWeight: 800, color: '#0f172a', marginBottom: 6 }}>
              🌱 Soil Conditioning Directives:
            </div>
            <ul style={{ paddingLeft: 18, fontSize: 13, color: '#475569', lineHeight: 1.6 }}>
              <li>Incorporate 5-8 tons/acre of well-decomposed Farm Yard Manure (FYM) annually.</li>
              <li>Practice crop rotation with pulses (Mung/Chickpea) to regenerate organic carbon.</li>
              <li>Mulch crop residues to preserve beneficial mycorrhiza and earthworm populations.</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
