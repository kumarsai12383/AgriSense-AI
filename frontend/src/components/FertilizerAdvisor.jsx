import React, { useState } from 'react';
import { FlaskConical, Leaf, Sparkles, AlertCircle, CheckCircle2, Calculator } from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { CROPS_DATA } from '../cropData';

export default function FertilizerAdvisor({ farmData, language, latestCrop }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;

  const [acres, setAcres] = useState(2);
  const [selectedCrop, setSelectedCrop] = useState(latestCrop?.crop || 'rice');

  const currentN = farmData?.nitrogen ?? 80;
  const currentP = farmData?.phosphorus ?? 40;
  const currentK = farmData?.potassium ?? 40;

  // Standard recommended NPK kg/ha targets
  const targetNPK = {
    rice: { n: 100, p: 50, k: 50 },
    maize: { n: 120, p: 60, k: 40 },
    cotton: { n: 120, p: 60, k: 60 },
    chickpea: { n: 20, p: 40, k: 20 },
    kidneybeans: { n: 80, p: 60, k: 40 },
    pigeonpeas: { n: 20, p: 50, k: 20 },
    banana: { n: 200, p: 60, k: 250 },
    watermelon: { n: 100, p: 60, k: 60 },
  };

  const cropReq = targetNPK[selectedCrop.toLowerCase()] || { n: 100, p: 50, k: 50 };

  // Calculate Fertilizer dosages per acre (1 Hectare = 2.47 Acres)
  const factor = acres / 2.47;
  const netN = Math.max(0, cropReq.n - (currentN * 0.4)) * factor;
  const netP = Math.max(0, cropReq.p - (currentP * 0.5)) * factor;
  const netK = Math.max(0, cropReq.k - (currentK * 0.5)) * factor;

  // Commercial bag conversions (Urea: 46% N, DAP: 18% N + 46% P, MOP: 60% K)
  const dapBags = Math.round((netP / 0.46) / 50 * 10) / 10;
  const nFromDap = (dapBags * 50) * 0.18;
  const remainingN = Math.max(0, netN - nFromDap);
  const ureaBags = Math.round((remainingN / 0.46) / 50 * 10) / 10;
  const mopBags = Math.round((netK / 0.60) / 50 * 10) / 10;

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #15803d 0%, #14532d 100%)',
          color: 'white',
          padding: '24px 28px',
          borderRadius: 20
        }}
      >
        <h2 style={{ color: 'white', fontSize: 24, margin: '0 0 6px 0' }}>
          {t.fertilizer.title}
        </h2>
        <p style={{ color: '#dcfce7', fontSize: 14, margin: 0, maxWidth: 650 }}>
          {t.fertilizer.subtitle}
        </p>
      </div>

      <div className="grid-2">
        {/* Controls */}
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <Calculator size={20} style={{ color: '#15803d' }} />
              <span>Field Specification</span>
            </div>
          </div>

          <div className="input-group">
            <label className="input-label">Target Crop</label>
            <select
              className="input-field"
              value={selectedCrop}
              onChange={(e) => setSelectedCrop(e.target.value)}
            >
              <option value="rice">Rice / Paddy</option>
              <option value="maize">Maize / Corn</option>
              <option value="cotton">Cotton</option>
              <option value="chickpea">Chickpea / Bengal Gram</option>
              <option value="kidneybeans">Kidney Beans / Rajma</option>
              <option value="pigeonpeas">Pigeon Pea / Tur</option>
              <option value="banana">Banana</option>
              <option value="watermelon">Watermelon</option>
            </select>
          </div>

          <div className="input-group">
            <label className="input-label">Land Area (Acres)</label>
            <input
              type="number"
              step="0.5"
              min="0.5"
              max="50"
              className="input-field"
              value={acres}
              onChange={(e) => setAcres(parseFloat(e.target.value) || 1)}
            />
          </div>

          <div style={{ background: '#f8fafc', padding: 14, borderRadius: 14, border: '1px solid #e2e8f0', marginTop: 14 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: '#64748b', marginBottom: 4 }}>
              Current Soil Baseline:
            </div>
            <div style={{ fontSize: 13, color: '#0f172a', fontWeight: 600 }}>
              N: {currentN} kg/ha • P: {currentP} kg/ha • K: {currentK} kg/ha
            </div>
          </div>
        </div>

        {/* Commercial Fertilizer Dosage Plan */}
        <div className="agri-card">
          <div className="agri-card-header">
            <div className="agri-card-title">
              <FlaskConical size={20} style={{ color: '#15803d' }} />
              <span>Recommended Commercial Dosage ({acres} Acres)</span>
            </div>
            <span className="badge badge-green">Custom Plan</span>
          </div>

          <div className="grid-responsive-3" style={{ margin: '14px 0 20px 0' }}>
            {/* Urea */}
            <div style={{ background: '#ecfdf5', padding: 14, borderRadius: 14, border: '1px solid #a7f3d0', textAlign: 'center' }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: '#065f46' }}>Urea (46% N)</div>
              <div style={{ fontSize: 24, fontWeight: 800, color: '#15803d', margin: '4px 0' }}>
                {ureaBags}
              </div>
              <div style={{ fontSize: 11, color: '#047857' }}>Bags (50kg)</div>
            </div>

            {/* DAP */}
            <div style={{ background: '#eff6ff', padding: 14, borderRadius: 14, border: '1px solid #bfdbfe', textAlign: 'center' }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: '#1e40af' }}>DAP (18:46:0)</div>
              <div style={{ fontSize: 24, fontWeight: 800, color: '#2563eb', margin: '4px 0' }}>
                {dapBags}
              </div>
              <div style={{ fontSize: 11, color: '#1d4ed8' }}>Bags (50kg)</div>
            </div>

            {/* MOP */}
            <div style={{ background: '#fef3c7', padding: 14, borderRadius: 14, border: '1px solid #fde68a', textAlign: 'center' }}>
              <div style={{ fontSize: 11, fontWeight: 700, color: '#92400e' }}>MOP (60% K)</div>
              <div style={{ fontSize: 24, fontWeight: 800, color: '#d97706', margin: '4px 0' }}>
                {mopBags}
              </div>
              <div style={{ fontSize: 11, color: '#b45309' }}>Bags (50kg)</div>
            </div>
          </div>

          {/* Organic Soil Enrichener Recommendation */}
          <div style={{ background: '#fffbeb', padding: 14, borderRadius: 14, border: '1px solid #fef3c7' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, fontWeight: 800, color: '#92400e', marginBottom: 4 }}>
              <Leaf size={15} />
              <span>Organic Manure Formulation:</span>
            </div>
            <div style={{ fontSize: 13, color: '#78350f', lineHeight: 1.5 }}>
              Apply <strong>{Math.round(acres * 2.5)} Tons</strong> of Farm Yard Manure (FYM) or <strong>{Math.round(acres * 0.8)} Tons</strong> of Vermicompost before final plowing + <strong>{Math.round(acres * 100)} kg</strong> Neem Cake to suppress root nematodes.
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
