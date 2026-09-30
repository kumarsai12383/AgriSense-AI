import React, { useState } from 'react';
import { 
  Building2, 
  Search, 
  ShieldCheck, 
  ExternalLink, 
  PhoneCall, 
  Sparkles, 
  CheckCircle2, 
  HelpCircle,
  FileText,
  Filter,
  Layers,
  Award,
  ChevronRight,
  Sun,
  Droplets,
  Tractor,
  CreditCard,
  HeartHandshake,
  Volume2,
  Square
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

const NATIONAL_SCHEMES_DATA = [
  {
    id: "pm_kisan",
    category: "income",
    name: "PM-KISAN (Pradhan Mantri Kisan Samman Nidhi)",
    benefit: "₹6,000 / year (Direct Bank Transfer in 3 equal instalments of ₹2,000)",
    eligibility: "All landholding farmer families with cultivable land in their revenue records.",
    documents: "Aadhaar Card, Land ownership papers (Pahani / 7/12 / Patta), Aadhaar-linked Bank Passbook.",
    portal: "https://pmkisan.gov.in",
    helpline: "155261 / 1800-115-526",
    badgeColor: "#166534",
    badgeBg: "#dcfce7",
    icon: "🌾"
  },
  {
    id: "pmfby",
    category: "insurance",
    name: "PMFBY (Pradhan Mantri Fasal Bima Yojana)",
    benefit: "Comprehensive crop insurance against droughts, floods, pests & natural disasters. Low premium: 2% (Kharif), 1.5% (Rabi), 5% (Horticulture).",
    eligibility: "All farmers growing notified crops in notified areas, including sharecroppers and tenant farmers.",
    documents: "Land record (ROR / LPC), Sowing Certificate, Bank passbook, Aadhaar.",
    portal: "https://pmfby.gov.in",
    helpline: "1800-180-1551",
    badgeColor: "#1e40af",
    badgeBg: "#dbeafe",
    icon: "🛡️"
  },
  {
    id: "kcc",
    category: "credit",
    name: "KCC (Kisan Credit Card)",
    benefit: "Low-interest institutional credit up to ₹3,00,000 at effective 4% interest rate. Collateral-free loan up to ₹1.60 Lakh.",
    eligibility: "All farmers, individual/joint borrowers, tenant farmers, SHGs.",
    documents: "Filled application form, Aadhaar/Voter ID, Land record certified by revenue authorities.",
    portal: "https://myscheme.gov.in/schemes/kcc",
    helpline: "1800-11-2211 / Nearest Bank",
    badgeColor: "#92400e",
    badgeBg: "#fef3c7",
    icon: "💳"
  },
  {
    id: "pm_kusum",
    category: "machinery",
    name: "PM-KUSUM Solar Agricultural Pumps",
    benefit: "Up to 60% Central + State subsidy for standalone solar pumps (3HP, 5HP, 7.5HP) + 30% bank loan. Farmer pays only 10% upfront!",
    eligibility: "Individual farmers, farmer groups, cooperatives, panchayats, FPOs.",
    documents: "Aadhaar Card, Land documents, Bank Passbook, Borewell NOC.",
    portal: "https://pmkusum.mnre.gov.in",
    helpline: "1800-180-3333",
    badgeColor: "#c2410c",
    badgeBg: "#ffedd5",
    icon: "☀️"
  },
  {
    id: "smam",
    category: "machinery",
    name: "SMAM (Sub-Mission on Agricultural Mechanization)",
    benefit: "40% to 80% government subsidy on Tractors, Power Tillers, Rotavators, Harvesters, Drone spraying equipment.",
    eligibility: "Small, marginal, SC/ST, and women farmers receive highest subsidy preference.",
    documents: "Aadhaar, Land documents, Bank details, Caste certificate (if applicable).",
    portal: "https://agrimachinery.nic.in",
    helpline: "1800-180-1551",
    badgeColor: "#4338ca",
    badgeBg: "#e0e7ff",
    icon: "🚜"
  },
  {
    id: "soil_health",
    category: "soil_water",
    name: "Soil Health Card Scheme",
    benefit: "Free lab testing of 12 soil parameters (N, P, K, pH, Micronutrients) + custom fertilizer dosage to cut costs by 15-25%.",
    eligibility: "Every agricultural landholder across all states in India.",
    documents: "Land record / Khata number, Soil sample from village officer.",
    portal: "https://soilhealth.dac.gov.in",
    helpline: "Contact Local Krishi Vigyan Kendra (KVK)",
    badgeColor: "#065f46",
    badgeBg: "#d1fae5",
    icon: "🧪"
  },
  {
    id: "pmksy",
    category: "soil_water",
    name: "PMKSY (Per Drop More Crop - Drip & Sprinkler)",
    benefit: "55% subsidy for Small/Marginal farmers and 45% for other farmers on Drip and Sprinkler systems. Saves 40% water, boosts yield by 30%.",
    eligibility: "Farmers with valid land ownership and an assured farm water source.",
    documents: "Aadhaar card, Land title deed, Water availability certificate.",
    portal: "https://pmksy.gov.in",
    helpline: "District Horticulture / Agriculture Officer",
    badgeColor: "#0369a1",
    badgeBg: "#e0f2fe",
    icon: "💧"
  },
  {
    id: "pkvy",
    category: "soil_water",
    name: "PKVY (Paramparagat Krishi Vikas Yojana - Organic Farming)",
    benefit: "Financial grant of ₹50,000 per hectare over 3 years for organic cluster farming, PGS organic certification, and marketing.",
    eligibility: "Groups of 20-50 farmers forming a 50-acre contiguous cluster.",
    documents: "Group formation resolution, Aadhaar copies, GPS coordinates.",
    portal: "https://pgsindia-ncof.gov.in",
    helpline: "State Agriculture Department",
    badgeColor: "#15803d",
    badgeBg: "#f0fdf4",
    icon: "🌱"
  }
];

const STATE_SCHEMES_MAP = {
  "Telangana": [
    { name: "Rythu Bandhu (Investment Support)", benefit: "₹10,000 per acre per year (₹5,000 Kharif + ₹5,000 Rabi) directly in bank account.", portal: "rythubandhu.telangana.gov.in" },
    { name: "Rythu Bima (Group Life Insurance)", benefit: "₹5,00,000 life insurance coverage for farmers aged 18-59 with 100% state-paid premium.", portal: "rythubima.telangana.gov.in" },
    { name: "24x7 Free Agricultural Power Supply", benefit: "Round-the-clock free uninterrupted 3-phase electricity for all farm pumps.", portal: "tssouthernpower.com" }
  ],
  "Andhra Pradesh": [
    { name: "YSR Rythu Bharosa - PM KISAN", benefit: "₹13,500/year per farmer family (₹6,000 PM-KISAN + ₹7,500 state grant). Covers tenant farmers.", portal: "ysrrythubharosa.ap.gov.in" },
    { name: "Free 9-Hours Daytime Agricultural Power", benefit: "100% free daytime electricity for irrigation pump-sets up to 10HP.", portal: "apcpdcl.in" },
    { name: "YSR Sunna Vaddi Panta Runalu", benefit: "Zero-interest crop loans up to ₹1,00,000 on prompt repayment.", portal: "apagrisnet.gov.in" }
  ],
  "Karnataka": [
    { name: "Raitha Siri Scheme", benefit: "₹10,000 per hectare incentive directly to millet-growing farmers.", portal: "raitamitra.karnataka.gov.in" },
    { name: "Krishi Bhagya", benefit: "Up to 80% subsidy for construction of Farm Ponds (Krishi Honda) with polythene lining and diesel pumps.", portal: "raitamitra.karnataka.gov.in" },
    { name: "Ganga Kalyana Scheme", benefit: "Free borewell drilling with submersible pump installation for SC/ST and OBC small/marginal farmers.", portal: "kmdc.karnataka.gov.in" }
  ],
  "Tamil Nadu": [
    { name: "Chief Minister's Uzhavar Pathukappu Thittam", benefit: "Comprehensive social security, accidental death assistance (₹1,00,000), monthly old-age pension.", portal: "tn.gov.in" },
    { name: "Free Agricultural Power & Solar Subsidy", benefit: "Free power for farm pumps + 70% subsidy for solar water pumping systems.", portal: "tangedco.gov.in" },
    { name: "Uzhavar Sandhai Direct Farm Marketing", benefit: "Free retail stalls in state markets to sell directly without middleman commissions.", portal: "agritech.tnau.ac.in" }
  ],
  "Maharashtra": [
    { name: "Namo Shetkari Mahasanman Nidhi Yojana", benefit: "Additional ₹6,000/year state grant on top of PM-KISAN (Total ₹12,000/year).", portal: "mahadbt.maharashtra.gov.in" },
    { name: "Magel Tyala Shet Tale (Farm Pond On Demand)", benefit: "Direct grant of up to ₹50,000 for digging farm pond to harvest rainwater.", portal: "krishi.maharashtra.gov.in" },
    { name: "Gopinath Munde Shetkari Apghat Vima", benefit: "₹2,00,000 accidental insurance cover with 100% state funded premium.", portal: "krishi.maharashtra.gov.in" }
  ]
};

export default function GovtSchemes({ farmer, language }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const sT = t.schemes || TRANSLATIONS.English.schemes;

  const [activeTab, setActiveTab] = useState('national'); // 'national' | 'state' | 'eligibility'
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [selectedState, setSelectedState] = useState(farmer?.state || "Telangana");

  // AI eligibility state
  const [farmSize, setFarmSize] = useState(farmer?.land_size || 2.0);
  const [farmerCategory, setFarmerCategory] = useState("Small / Marginal Farmer (< 5 acres)");
  const [primaryCrop, setPrimaryCrop] = useState("Cotton");
  const [aiChecking, setAiChecking] = useState(false);
  const [aiResult, setAiResult] = useState(null);
  const [speakingSchemeId, setSpeakingSchemeId] = useState(null);

  const handleSpeakSchemeText = (schemeId, text) => {
    if (!('speechSynthesis' in window)) return;
    if (speakingSchemeId === schemeId) {
      window.speechSynthesis.cancel();
      setSpeakingSchemeId(null);
      return;
    }
    window.speechSynthesis.cancel();
    const cleanText = text.replace(/[*#_`]/g, '').trim();
    const utterance = new SpeechSynthesisUtterance(cleanText);
    const langMap = {
      'తెలుగు': 'te-IN', 'Telugu': 'te-IN',
      'हिंदी': 'hi-IN', 'Hindi': 'hi-IN',
      'தமிழ்': 'ta-IN', 'Tamil': 'ta-IN',
      'ಕನ್ನಡ': 'kn-IN', 'Kannada': 'kn-IN',
      'मराठी': 'mr-IN', 'Marathi': 'mr-IN',
      'English': 'en-IN'
    };
    const targetTag = langMap[language] || 'en-IN';
    utterance.lang = targetTag;
    utterance.rate = 0.92;

    const voices = window.speechSynthesis.getVoices() || [];
    const matchedVoice = voices.find(v => v.lang.toLowerCase() === targetTag.toLowerCase())
      || voices.find(v => v.lang.toLowerCase().startsWith(targetTag.split('-')[0]))
      || voices.find(v => v.name.toLowerCase().includes(language.toLowerCase()));

    if (matchedVoice) utterance.voice = matchedVoice;

    utterance.onend = () => setSpeakingSchemeId(null);
    utterance.onerror = () => setSpeakingSchemeId(null);

    setSpeakingSchemeId(schemeId);
    window.speechSynthesis.speak(utterance);
  };

  // Filter schemes
  const filteredSchemes = NATIONAL_SCHEMES_DATA.filter(sc => {
    const matchesSearch = sc.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          sc.benefit.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCat = categoryFilter === 'all' || sc.category === categoryFilter;
    return matchesSearch && matchesCat;
  });

  const handleAiEligibilityCheck = async () => {
    setAiChecking(true);
    setAiResult(null);
    const query = 
      `Check government scheme eligibility for an Indian farmer with:\n` +
      `- Land Size: ${farmSize} acres (${farmerCategory})\n` +
      `- State: ${selectedState}\n` +
      `- Primary Crop: ${primaryCrop}\n\n` +
      `Provide a personalized list of all Central and State government schemes they qualify for, exact subsidy amounts (₹), mandatory documents required (e.g. e-KYC, NPCI seeding), and step-by-step application instructions.`;
    
    try {
      const res = await api.askAi(farmer?.id || 1, query, language);
      if (res && res.answer) {
        setAiResult(res.answer);
      } else {
        throw new Error("No response");
      }
    } catch (err) {
      setAiResult(
        `### 🌟 Personalized Scheme Eligibility Report for ${farmer?.name || "Farmer"}\n\n` +
        `Based on your **${farmSize} acre** farm in **${selectedState}**, you qualify for:\n\n` +
        `1. **PM-KISAN:** ₹6,000/year (100% eligible, ensure Aadhaar e-KYC is completed)\n` +
        `2. **PM-KUSUM Solar Pump:** 60% combined Central + State subsidy for a 3HP/5HP solar pump.\n` +
        `3. **PMKSY Micro-Irrigation:** 55% subsidy on Drip & Sprinkler irrigation.\n` +
        `4. **PMFBY Crop Insurance:** Sum insured against weather calamities at 2% premium.\n` +
        `5. **Kisan Credit Card (KCC):** Up to ₹3,00,000 crop loan at effective 4% interest rate.\n\n` +
        `📄 **Key Documents Needed:** Aadhaar Card, Land Patta/Pahani/7-12, Bank Passbook linked with NPCI mapper.`
      );
    } finally {
      setAiChecking(false);
    }
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24 }}>
      {/* Hero Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #064e3b 0%, #047857 50%, #0f766e 100%)',
          color: 'white',
          padding: '26px 30px',
          borderRadius: 24,
          boxShadow: '0 12px 30px -5px rgba(4, 120, 87, 0.35)'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, background: 'rgba(255,255,255,0.2)', padding: '4px 12px', borderRadius: 99, fontSize: 11, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 8 }}>
              <Building2 size={14} />
              <span>Ministry of Agriculture & Farmers Welfare | Govt. of India</span>
            </div>
            <h1 style={{ color: 'white', fontSize: 26, fontWeight: 800, margin: '4px 0 6px 0' }}>
              {sT.title}
            </h1>
            <p style={{ color: '#d1fae5', fontSize: 14, margin: 0, fontWeight: 500 }}>
              {sT.subtitle}
            </p>
          </div>
          <div style={{ fontSize: 44 }}>🏛️</div>
        </div>

        {/* Emergency Helpline Strip */}
        <div style={{
          marginTop: 18,
          background: 'rgba(255, 255, 255, 0.12)',
          border: '1px solid rgba(255, 255, 255, 0.25)',
          borderRadius: 14,
          padding: '10px 18px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 10
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <PhoneCall size={18} color="#fef08a" />
            <span style={{ fontWeight: 800, fontSize: 13, color: '#fef08a' }}>
              Farmer Welfare Toll-Free Helpline: 1800-180-1551 / 155261 (6 AM - 10 PM)
            </span>
          </div>
          <a 
            href="tel:18001801551" 
            className="btn"
            style={{ background: '#ffffff', color: '#064e3b', fontWeight: 800, fontSize: 12, padding: '6px 14px', borderRadius: 10, textDecoration: 'none' }}
          >
            Call 1800-180-1551 📞
          </a>
        </div>
      </div>

      {/* Main Tab Switcher */}
      <div style={{ display: 'flex', gap: 12, borderBottom: '2px solid #e2e8f0', paddingBottom: 8, flexWrap: 'wrap' }}>
        <button
          onClick={() => setActiveTab('national')}
          className="btn"
          style={{
            background: activeTab === 'national' ? '#047857' : '#ffffff',
            color: activeTab === 'national' ? '#ffffff' : '#64748b',
            border: '1.5px solid',
            borderColor: activeTab === 'national' ? '#047857' : '#cbd5e1',
            fontWeight: 800,
            borderRadius: 12,
            padding: '10px 20px'
          }}
        >
          <Award size={18} />
          <span>{sT.tabNational}</span>
        </button>

        <button
          onClick={() => setActiveTab('state')}
          className="btn"
          style={{
            background: activeTab === 'state' ? '#1e40af' : '#ffffff',
            color: activeTab === 'state' ? '#ffffff' : '#64748b',
            border: '1.5px solid',
            borderColor: activeTab === 'state' ? '#1e40af' : '#cbd5e1',
            fontWeight: 800,
            borderRadius: 12,
            padding: '10px 20px'
          }}
        >
          <Building2 size={18} />
          <span>{sT.tabState}</span>
        </button>

        <button
          onClick={() => setActiveTab('eligibility')}
          className="btn"
          style={{
            background: activeTab === 'eligibility' ? '#7c3aed' : '#ffffff',
            color: activeTab === 'eligibility' ? '#ffffff' : '#64748b',
            border: '1.5px solid',
            borderColor: activeTab === 'eligibility' ? '#7c3aed' : '#cbd5e1',
            fontWeight: 800,
            borderRadius: 12,
            padding: '10px 20px'
          }}
        >
          <Sparkles size={18} />
          <span>{sT.tabEligibility}</span>
        </button>
      </div>

      {/* TAB 1: NATIONAL SCHEMES */}
      {activeTab === 'national' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          {/* Search & Category Filter Bar */}
          <div className="agri-card" style={{ padding: 18, borderRadius: 18, display: 'flex', flexDirection: 'column', gap: 14 }}>
            <div style={{ position: 'relative' }}>
              <Search size={18} style={{ position: 'absolute', left: 14, top: 12, color: '#94a3b8' }} />
              <input 
                type="text" 
                placeholder={sT.searchPlaceholder}
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="input-field"
                style={{ width: '100%', paddingLeft: 42, borderRadius: 12, border: '1.5px solid #cbd5e1', fontSize: 14 }}
              />
            </div>

            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              <button 
                onClick={() => setCategoryFilter('all')}
                className="btn"
                style={{
                  background: categoryFilter === 'all' ? '#1e293b' : '#f1f5f9',
                  color: categoryFilter === 'all' ? '#ffffff' : '#475569',
                  fontSize: 12,
                  fontWeight: 700,
                  borderRadius: 20,
                  padding: '6px 14px'
                }}
              >
                All Schemes ({NATIONAL_SCHEMES_DATA.length})
              </button>
              <button 
                onClick={() => setCategoryFilter('income')}
                className="btn"
                style={{
                  background: categoryFilter === 'income' ? '#166534' : '#f1f5f9',
                  color: categoryFilter === 'income' ? '#ffffff' : '#475569',
                  fontSize: 12,
                  fontWeight: 700,
                  borderRadius: 20,
                  padding: '6px 14px'
                }}
              >
                Direct Income (₹)
              </button>
              <button 
                onClick={() => setCategoryFilter('insurance')}
                className="btn"
                style={{
                  background: categoryFilter === 'insurance' ? '#1e40af' : '#f1f5f9',
                  color: categoryFilter === 'insurance' ? '#ffffff' : '#475569',
                  fontSize: 12,
                  fontWeight: 700,
                  borderRadius: 20,
                  padding: '6px 14px'
                }}
              >
                Crop Insurance 🛡️
              </button>
              <button 
                onClick={() => setCategoryFilter('machinery')}
                className="btn"
                style={{
                  background: categoryFilter === 'machinery' ? '#c2410c' : '#f1f5f9',
                  color: categoryFilter === 'machinery' ? '#ffffff' : '#475569',
                  fontSize: 12,
                  fontWeight: 700,
                  borderRadius: 20,
                  padding: '6px 14px'
                }}
              >
                Solar & Machinery 🚜
              </button>
              <button 
                onClick={() => setCategoryFilter('credit')}
                className="btn"
                style={{
                  background: categoryFilter === 'credit' ? '#92400e' : '#f1f5f9',
                  color: categoryFilter === 'credit' ? '#ffffff' : '#475569',
                  fontSize: 12,
                  fontWeight: 700,
                  borderRadius: 20,
                  padding: '6px 14px'
                }}
              >
                Kisan Credit Card 💳
              </button>
              <button 
                onClick={() => setCategoryFilter('soil_water')}
                className="btn"
                style={{
                  background: categoryFilter === 'soil_water' ? '#0369a1' : '#f1f5f9',
                  color: categoryFilter === 'soil_water' ? '#ffffff' : '#475569',
                  fontSize: 12,
                  fontWeight: 700,
                  borderRadius: 20,
                  padding: '6px 14px'
                }}
              >
                Soil & Water 💧
              </button>
            </div>
          </div>

          {/* Scheme Cards Grid */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 300px), 1fr))', gap: 16 }}>
            {filteredSchemes.map(scheme => (
              <div 
                key={scheme.id}
                className="agri-card"
                style={{
                  padding: 22,
                  borderRadius: 18,
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  border: `1.5px solid ${scheme.badgeColor}33`,
                  boxShadow: '0 4px 12px rgba(0,0,0,0.03)'
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 8, marginBottom: 12 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <span style={{ fontSize: 24 }}>{scheme.icon}</span>
                      <h3 style={{ fontSize: 16, fontWeight: 800, color: '#1e293b', margin: 0, lineHeight: 1.3 }}>
                        {scheme.name}
                      </h3>
                    </div>

                    {/* 🔊 Speak Scheme Button */}
                    <button
                      type="button"
                      onClick={() => handleSpeakSchemeText(
                        scheme.id,
                        `Scheme: ${scheme.name}. Benefit: ${scheme.benefit}. Eligibility: ${scheme.eligibility}. Documents: ${scheme.documents}. Helpline: ${scheme.helpline}.`
                      )}
                      className="btn btn-secondary"
                      style={{
                        padding: '5px 10px',
                        borderRadius: 10,
                        fontSize: 11.5,
                        fontWeight: 800,
                        color: speakingSchemeId === scheme.id ? '#dc2626' : '#15803d',
                        borderColor: speakingSchemeId === scheme.id ? '#fca5a5' : '#86efac',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: 4,
                        flexShrink: 0
                      }}
                      title="Listen to Scheme"
                    >
                      {speakingSchemeId === scheme.id ? <Square size={13} /> : <Volume2 size={13} />}
                      <span>{speakingSchemeId === scheme.id ? 'Stop' : '🔊 Listen'}</span>
                    </button>
                  </div>

                  <div style={{ background: scheme.badgeBg, color: scheme.badgeColor, padding: '10px 14px', borderRadius: 12, fontSize: 13, fontWeight: 700, marginBottom: 12 }}>
                    💰 {scheme.benefit}
                  </div>

                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8, fontSize: 13, color: '#475569', marginBottom: 16 }}>
                    <div>
                      <strong style={{ color: '#1e293b' }}>🎯 Eligibility: </strong>
                      {scheme.eligibility}
                    </div>
                    <div>
                      <strong style={{ color: '#1e293b' }}>📄 Required Documents: </strong>
                      {scheme.documents}
                    </div>
                    <div>
                      <strong style={{ color: '#1e293b' }}>📞 Helpline: </strong>
                      {scheme.helpline}
                    </div>
                  </div>
                </div>

                <div style={{ display: 'flex', gap: 8 }}>
                  <a 
                    href={scheme.portal}
                    target="_blank"
                    rel="noreferrer"
                    className="btn"
                    style={{
                      flex: 1,
                      background: scheme.badgeColor,
                      color: 'white',
                      fontWeight: 800,
                      fontSize: 13,
                      padding: '10px 14px',
                      borderRadius: 12,
                      textDecoration: 'none',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: 6
                    }}
                  >
                    <span>Apply on Portal</span>
                    <ExternalLink size={14} />
                  </a>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* TAB 2: STATE WELFARE SCHEMES */}
      {activeTab === 'state' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div className="agri-card" style={{ padding: 22, borderRadius: 20 }}>
            <h3 style={{ fontSize: 18, fontWeight: 800, color: '#1e293b', marginBottom: 14 }}>
              📍 Select State for Tailored State Welfare & Subsidies
            </h3>

            <div style={{ maxWidth: 400 }}>
              <select 
                value={selectedState} 
                onChange={(e) => setSelectedState(e.target.value)}
                className="input-field"
                style={{ width: '100%', padding: '10px 14px', borderRadius: 12, border: '1.5px solid #cbd5e1', fontWeight: 700 }}
              >
                {Object.keys(STATE_SCHEMES_MAP).map(st => (
                  <option key={st} value={st}>{st}</option>
                ))}
              </select>
            </div>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 280px), 1fr))', gap: 16 }}>
            {(STATE_SCHEMES_MAP[selectedState] || []).map((sc, i) => {
              const stateSchemeKey = `state_${selectedState}_${i}`;
              const isSpeaking = speakingSchemeId === stateSchemeKey;
              return (
                <div 
                  key={i}
                  className="agri-card"
                  style={{ padding: 20, borderRadius: 16, border: '1.5px solid #93c5fd' }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: 8, marginBottom: 8 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                      <Award size={20} color="#1e40af" />
                      <h4 style={{ fontSize: 16, fontWeight: 800, color: '#1e40af', margin: 0 }}>
                        {sc.name}
                      </h4>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleSpeakSchemeText(stateSchemeKey, `State scheme: ${sc.name}. Benefit: ${sc.benefit}. Official Portal: ${sc.portal}`)}
                      className="btn btn-secondary"
                      style={{
                        padding: '4px 8px',
                        borderRadius: 8,
                        fontSize: 11,
                        fontWeight: 800,
                        color: isSpeaking ? '#dc2626' : '#1e40af',
                        borderColor: isSpeaking ? '#fca5a5' : '#bfdbfe',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: 4
                      }}
                      title="Listen to Scheme"
                    >
                      {isSpeaking ? <Square size={12} /> : <Volume2 size={12} />}
                      <span>{isSpeaking ? 'Stop' : '🔊'}</span>
                    </button>
                  </div>

                  <div style={{ background: '#eff6ff', color: '#1e3a8a', padding: '10px 12px', borderRadius: 10, fontSize: 13, fontWeight: 600, marginBottom: 12 }}>
                    💰 {sc.benefit}
                  </div>

                  <div style={{ fontSize: 12, color: '#64748b' }}>
                    Official Portal: <strong style={{ color: '#1e40af' }}>{sc.portal}</strong>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* TAB 3: INSTANT AI ELIGIBILITY CHECKER */}
      {activeTab === 'eligibility' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
          <div className="agri-card" style={{ padding: 24, borderRadius: 20 }}>
            <h3 style={{ fontSize: 18, fontWeight: 800, color: '#1e293b', marginBottom: 16 }}>
              🎯 Instant AI Scheme Eligibility & Subsidy Advisor
            </h3>

            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 200px), 1fr))', gap: 16 }}>
              <div>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 700, color: '#475569', marginBottom: 6 }}>
                  Farm Size (Acres)
                </label>
                <input 
                  type="number" 
                  step="0.5" 
                  min="0.5" 
                  max="500" 
                  value={farmSize} 
                  onChange={(e) => setFarmSize(e.target.value)}
                  className="input-field"
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 12, border: '1.5px solid #cbd5e1', fontWeight: 600 }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 700, color: '#475569', marginBottom: 6 }}>
                  Farmer Category
                </label>
                <select 
                  value={farmerCategory} 
                  onChange={(e) => setFarmerCategory(e.target.value)}
                  className="input-field"
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 12, border: '1.5px solid #cbd5e1', fontWeight: 600 }}
                >
                  <option value="Small / Marginal Farmer (< 5 acres)">Small / Marginal Farmer (&lt; 5 acres)</option>
                  <option value="Medium Farmer (5-10 acres)">Medium Farmer (5-10 acres)</option>
                  <option value="Large Farmer (> 10 acres)">Large Farmer (&gt; 10 acres)</option>
                  <option value="Women Farmer">Women Farmer</option>
                  <option value="Tenant / Sharecropper">Tenant / Sharecropper</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: 13, fontWeight: 700, color: '#475569', marginBottom: 6 }}>
                  Primary Crop
                </label>
                <input 
                  type="text" 
                  value={primaryCrop} 
                  onChange={(e) => setPrimaryCrop(e.target.value)}
                  className="input-field"
                  style={{ width: '100%', padding: '10px 14px', borderRadius: 12, border: '1.5px solid #cbd5e1', fontWeight: 600 }}
                />
              </div>
            </div>

            <button
              onClick={handleAiEligibilityCheck}
              disabled={aiChecking}
              className="btn btn-primary"
              style={{
                width: '100%',
                marginTop: 20,
                background: 'linear-gradient(135deg, #7c3aed 0%, #6d28d9 100%)',
                color: 'white',
                fontWeight: 800,
                fontSize: 15,
                padding: '14px 20px',
                borderRadius: 14
              }}
            >
              <Sparkles size={18} />
              <span>{aiChecking ? "⏳ Evaluating Ministry Guidelines..." : sT.checkBtn}</span>
            </button>
          </div>

          {/* AI Output Card */}
          {aiResult && (
            <div className="agri-card" style={{ padding: 24, borderRadius: 20, background: '#faf5ff', border: '2px solid #d8b4fe' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10, marginBottom: 12 }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  <Sparkles size={20} color="#7c3aed" />
                  <h3 style={{ fontSize: 17, fontWeight: 800, color: '#6b21a8', margin: 0 }}>
                    🤖 Personalized Scheme & Subsidy Report
                  </h3>
                </div>

                <button
                  type="button"
                  onClick={() => handleSpeakSchemeText('ai_report', aiResult)}
                  className="btn btn-secondary"
                  style={{
                    padding: '6px 14px',
                    borderRadius: 10,
                    fontSize: 12,
                    fontWeight: 800,
                    color: speakingSchemeId === 'ai_report' ? '#dc2626' : '#7c3aed',
                    borderColor: speakingSchemeId === 'ai_report' ? '#fca5a5' : '#d8b4fe',
                    display: 'inline-flex',
                    alignItems: 'center',
                    gap: 6
                  }}
                >
                  {speakingSchemeId === 'ai_report' ? <Square size={14} /> : <Volume2 size={14} />}
                  <span>{speakingSchemeId === 'ai_report' ? 'Stop Voice' : '🔊 Listen to Report'}</span>
                </button>
              </div>
              <div style={{ whiteSpace: 'pre-wrap', fontSize: 14, lineHeight: 1.6, color: '#1e293b' }}>
                {aiResult}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
