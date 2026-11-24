import React, { useState } from 'react';
import { 
  HelpCircle, 
  Volume2, 
  Square, 
  ArrowRight, 
  PhoneCall, 
  CheckCircle2, 
  XCircle, 
  AlertTriangle,
  FileDown,
  Sparkles,
  Layers,
  Activity,
  Droplets,
  Wheat,
  Stethoscope,
  Mic,
  Cpu
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';

const STEP_DETAILS = [
  {
    num: "1",
    icon: "🌐",
    title: "Select Language & Login",
    desc: "Choose your mother tongue (Telugu, Hindi, Tamil, Kannada, Marathi, English) at the top. Enter your name and 10-digit mobile number to open your farm dashboard.",
    speech: "Step 1: Choose your language at the top right corner. Enter your name and mobile number, then tap Enter Dashboard.",
    target: "dashboard"
  },
  {
    num: "2",
    icon: "📡",
    title: "Enter Soil Data or Connect ESP32 Sensor",
    desc: "Open 'My Farm Data'. Standard soil readings are pre-filled. Adjust Nitrogen, Phosphorus, Potash, pH, and Moisture, or plug in your 7-in-1 sensor to sync live.",
    speech: "Step 2: In My Farm Data, default soil values are pre-filled. You can save your soil test values or connect the ESP32 probe to read live values.",
    target: "sensors"
  },
  {
    num: "3",
    icon: "🌾",
    title: "Get AI Crop Recommendation",
    desc: "Tap 'Find Best Crop'. The AI analyzes your soil and weather to recommend the highest-yielding crop with top alternatives and confidence percentages.",
    speech: "Step 3: In AI Crop Recommendation, tap Find Best Crop to see the most profitable crop suited for your soil and season.",
    target: "crop"
  },
  {
    num: "4",
    icon: "💧",
    title: "Check Smart Irrigation & Motor Time",
    desc: "Open 'Smart Irrigation'. Check the moisture meter: Red means water today, Green means soil is moist. Use the calculator to see exact pumping hours.",
    speech: "Step 4: In Smart Irrigation, Red means urgent watering needed today. Green means safe. Check the calculator for exact motor hours.",
    target: "irrigation"
  },
  {
    num: "5",
    icon: "🌿",
    title: "Follow 4-Stage Fertilizer Schedule",
    desc: "Open 'Fertilizer Guidance'. View soil NPK deficits and follow the 4-stage split dose table (Sowing, Tillering, Flowering, Grain filling) to save fertilizer cost.",
    speech: "Step 5: In Fertilizer Guidance, check how many bags of Urea, DAP, and Potash are needed across 4 crop growth stages.",
    target: "fertilizer"
  },
  {
    num: "6",
    icon: "🦠",
    title: "Diagnose Plant Diseases (Leaf Doctor)",
    desc: "If crop leaves have spots or yellowing, take a clear photo in daylight. The AI leaf doctor identifies the disease and gives organic and chemical remedies.",
    speech: "Step 6: In Plant Disease Doctor, take a daylight photo of the sick leaf. The AI will instantly tell you the disease name and medicine dosage.",
    target: "disease"
  },
  {
    num: "7",
    icon: "🤖🎙️",
    title: "Speak to AgriSense AI by Voice or Call",
    desc: "Tap the microphone button and speak in your language. Ask about weather, seeds, mandi rates, or crop pests to get instant spoken advice.",
    speech: "Step 7: In AgriSense AI Chat and Voice, press the green microphone and speak naturally in your mother tongue for instant spoken advice.",
    target: "voice"
  }
];

const COLOR_GUIDES = [
  { color: "#ef4444", bg: "#fef2f2", border: "#fca5a5", icon: "🔴", name: "RED (Urgent Action)", desc: "Soil is Dry / Water Immediately / Disease Detected / High Nutrient Deficit" },
  { color: "#eab308", bg: "#fefce8", border: "#fde047", icon: "🟡", name: "YELLOW (Warning / Watch)", desc: "Soil moisture dropping / Water within 2 days / Moderate nutrient level" },
  { color: "#22c55e", bg: "#f0fdf4", border: "#86efac", icon: "🟢", name: "GREEN (Safe / Healthy)", desc: "Soil is Moist & Optimal / Crop is Healthy / No immediate action needed" },
  { color: "#0284c7", bg: "#f0f9ff", border: "#7dd3fc", icon: "💧", name: "BLUE WATER DROP", desc: "Shows water liters needed and exact motor pumping runtime in hours" },
  { color: "#16a34a", bg: "#f0fdf4", border: "#86efac", icon: "🌿", name: "GREEN LEAF & BAG", desc: "Shows exact fertilizer bags (Urea, DAP, Potash) for your farm acreage" },
  { color: "#7c3aed", bg: "#faf5ff", border: "#d8b4fe", icon: "🎤", name: "PURPLE MICROPHONE", desc: "Tap and speak your question in your regional language with zero typing" }
];

export default function HelpCenter({ language, setCurrentTab }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const hT = t.help || TRANSLATIONS.English.help;
  const [isPlayingAll, setIsPlayingAll] = useState(false);
  const [speakingStep, setSpeakingStep] = useState(null);

  const langMap = {
    "English": "en-IN",
    "తెలుగు": "te-IN",
    "हिंदी": "hi-IN",
    "தமிழ்": "ta-IN",
    "ಕನ್ನಡ": "kn-IN",
    "मराठी": "mr-IN"
  };

  const speakText = (text, stepIdx = null) => {
    if (!('speechSynthesis' in window)) return;
    window.speechSynthesis.cancel();

    if (stepIdx !== null && speakingStep === stepIdx) {
      setSpeakingStep(null);
      return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = langMap[language] || "en-IN";
    utterance.rate = 0.95;

    utterance.onend = () => {
      setSpeakingStep(null);
      setIsPlayingAll(false);
    };

    setSpeakingStep(stepIdx);
    window.speechSynthesis.speak(utterance);
  };

  const playFullWalkthrough = () => {
    if (isPlayingAll) {
      window.speechSynthesis.cancel();
      setIsPlayingAll(false);
      setSpeakingStep(null);
      return;
    }

    const fullScript = "Welcome to AgriSense AI Farmer Guide. " + STEP_DETAILS.map(s => s.speech).join(" ");
    setIsPlayingAll(true);
    speakText(fullScript, null);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24,paddingTop: 125, margin: '0 auto', width: '100%' }}>
      {/* Hero Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #1e293b 0%, #0f172a 60%, #1e3a8a 100%)',
          color: 'white',
          padding: '26px 30px',
          borderRadius: 24,
          boxShadow: '0 12px 30px -5px rgba(15, 23, 42, 0.45)'
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 16 }}>
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: 6, background: 'rgba(255,255,255,0.15)', padding: '4px 12px', borderRadius: 99, fontSize: 11, fontWeight: 800, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 8 }}>
              <HelpCircle size={14} />
              <span>Easy Farmer Visual & Audio Walkthrough</span>
            </div>
            <h1 style={{ color: 'white', fontSize: 26, fontWeight: 800, margin: '4px 0 6px 0' }}>
              {hT.title}
            </h1>
            <p style={{ color: '#cbd5e1', fontSize: 14, margin: 0, fontWeight: 500 }}>
              {hT.subtitle}
            </p>
          </div>
          <div style={{ fontSize: 44 }}>👨‍🌾</div>
        </div>

        {/* Full Audio Guide Player Button */}
        <div style={{
          marginTop: 18,
          background: 'rgba(255, 255, 255, 0.08)',
          border: '1.5px solid rgba(255, 255, 255, 0.2)',
          borderRadius: 16,
          padding: '14px 20px',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: 12
        }}>
          <div>
            <div style={{ fontWeight: 800, fontSize: 14, color: '#4ade80' }}>
              🔊 Listen to Complete Audio Guide (Spoken Walkthrough)
            </div>
            <div style={{ fontSize: 12, color: '#94a3b8', marginTop: 2 }}>
              No reading needed — tap the play button to hear how to use each feature
            </div>
          </div>
          <button 
            onClick={playFullWalkthrough}
            className="btn"
            style={{
              background: isPlayingAll ? '#dc2626' : '#22c55e',
              color: 'white',
              fontWeight: 800,
              fontSize: 14,
              padding: '10px 20px',
              borderRadius: 12
            }}
          >
            {isPlayingAll ? <Square size={16} /> : <Volume2 size={16} />}
            <span>{isPlayingAll ? "⏹ Stop Audio Guide" : "🔊 Play Full Guide"}</span>
          </button>
        </div>
      </div>

      {/* 7-Step Workflow */}
      <div className="agri-card" style={{ padding: 24, borderRadius: 20 }}>
        <h3 style={{ fontSize: 19, fontWeight: 800, color: '#1e293b', marginBottom: 18 }}>
          {hT.workflowTitle}
        </h3>

        <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
          {STEP_DETAILS.map((step, idx) => (
            <div 
              key={idx}
              style={{
                background: '#f8fafc',
                border: '1.5px solid #e2e8f0',
                borderRadius: 16,
                padding: '16px 20px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                flexWrap: 'wrap',
                gap: 12
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', gap: 14, flex: '1 1 200px', minWidth: 0 }}>
                <div style={{
                  width: 38,
                  height: 38,
                  borderRadius: 12,
                  background: '#15803d',
                  color: 'white',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontWeight: 800,
                  fontSize: 16,
                  flexShrink: 0
                }}>
                  {step.num}
                </div>
                <div style={{ minWidth: 0, flex: 1 }}>
                  <div style={{ fontWeight: 800, fontSize: 15, color: '#1e293b' }}>
                    {step.title}
                  </div>
                  <div style={{ fontSize: 13, color: '#64748b', marginTop: 2, lineHeight: 1.4 }}>
                    {step.desc}
                  </div>
                </div>
              </div>

              <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
                <button
                  onClick={() => speakText(step.speech, idx)}
                  className="btn"
                  style={{
                    background: speakingStep === idx ? '#dc2626' : '#eff6ff',
                    color: speakingStep === idx ? '#ffffff' : '#1e40af',
                    border: '1px solid #93c5fd',
                    padding: '8px 14px',
                    borderRadius: 10,
                    fontSize: 12,
                    fontWeight: 700
                  }}
                >
                  <Volume2 size={14} />
                  <span>{speakingStep === idx ? "Stop" : "Listen"}</span>
                </button>

                <button
                  onClick={() => setCurrentTab(step.target)}
                  className="btn"
                  style={{
                    background: '#15803d',
                    color: 'white',
                    padding: '8px 14px',
                    borderRadius: 10,
                    fontSize: 12,
                    fontWeight: 700
                  }}
                >
                  <span>Open Page</span>
                  <ArrowRight size={14} />
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Traffic Light Color Guide */}
      <div className="agri-card" style={{ padding: 24, borderRadius: 20 }}>
        <h3 style={{ fontSize: 18, fontWeight: 800, color: '#1e293b', marginBottom: 16 }}>
          {hT.colorsTitle}
        </h3>

        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 240px), 1fr))', gap: 14 }}>
          {COLOR_GUIDES.map((cg, i) => (
            <div 
              key={i}
              style={{
                background: cg.bg,
                border: `1.5px solid ${cg.border}`,
                borderRadius: 14,
                padding: '14px 16px',
                display: 'flex',
                alignItems: 'flex-start',
                gap: 10
              }}
            >
              <span style={{ fontSize: 20 }}>{cg.icon}</span>
              <div>
                <div style={{ fontWeight: 800, fontSize: 13, color: cg.color }}>
                  {cg.name}
                </div>
                <div style={{ fontSize: 12, color: '#475569', marginTop: 2 }}>
                  {cg.desc}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Dos & Don'ts */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 280px), 1fr))', gap: 18 }}>
        <div className="agri-card" style={{ padding: 22, borderRadius: 20, border: '1.5px solid #86efac' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <CheckCircle2 size={20} color="#15803d" />
            <h3 style={{ fontSize: 16, fontWeight: 800, color: '#166534', margin: 0 }}>
              ✅ Recommended Farming Best Practices
            </h3>
          </div>
          <ul style={{ paddingLeft: 18, margin: 0, fontSize: 13, lineHeight: 1.7, color: '#334155' }}>
            <li>Conduct soil lab tests once every 2 years for accurate NPK baseline.</li>
            <li>Irrigate in the early morning (6-8 AM) or evening to minimize water evaporation.</li>
            <li>Split fertilizer application into 4 stages rather than a single heavy dose.</li>
            <li>Take leaf disease photos in bright morning sunlight for 99% AI accuracy.</li>
          </ul>
        </div>

        <div className="agri-card" style={{ padding: 22, borderRadius: 20, border: '1.5px solid #fca5a5' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 14 }}>
            <XCircle size={20} color="#dc2626" />
            <h3 style={{ fontSize: 16, fontWeight: 800, color: '#991b1b', margin: 0 }}>
              ❌ Practices to Avoid
            </h3>
          </div>
          <ul style={{ paddingLeft: 18, margin: 0, fontSize: 13, lineHeight: 1.7, color: '#334155' }}>
            <li>Do not over-apply Urea without testing soil Phosphorus and Potash levels.</li>
            <li>Avoid flood irrigation when soil moisture is already above 50%.</li>
            <li>Do not spray pesticides during peak afternoon heat or strong winds.</li>
            <li>Avoid delaying PMFBY crop loss intimation past the mandatory 72-hour deadline.</li>
          </ul>
        </div>
      </div>

      {/* Emergency Helpline Strip */}
      <div className="agri-card" style={{ padding: 20, borderRadius: 18, background: '#fef3c7', border: '2px solid #fde68a', display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: 28 }}>📞</span>
          <div>
            <div style={{ fontWeight: 800, fontSize: 15, color: '#92400e' }}>
              Government Kisan Helpline (Toll-Free): 1551 / 1800-180-1551
            </div>
            <div style={{ fontSize: 12, color: '#78350f' }}>
              Direct agricultural scientist support from 6:00 AM to 10:00 PM all 7 days
            </div>
          </div>
        </div>
        <a 
          href="tel:1551" 
          className="btn"
          style={{ background: '#b45309', color: 'white', fontWeight: 800, fontSize: 13, padding: '8px 18px', borderRadius: 10, textDecoration: 'none' }}
        >
          Call 1551 📞
        </a>
      </div>
    </div>
  );
}
