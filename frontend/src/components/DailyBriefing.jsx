import React, { useState, useEffect, useRef } from 'react';
import {
  Volume2, VolumeX, Play, Pause, Square, RefreshCw, Sparkles,
  TrendingUp, Wheat, ShieldAlert, Lightbulb, Clock, CheckCircle2,
  Calendar, Droplets, ChevronDown, ChevronUp, Edit3, X, Save
} from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

const MANDI_RATES_CLIENT = {
  "rice": { name: "Rice (Paddy)", price: "₹2,350 / q", trend: "📈 +1.8% Up", msp: "₹2,300/q", action: "Steady buyer demand in local APMC." },
  "paddy": { name: "Paddy (Rice)", price: "₹2,350 / q", trend: "📈 +1.8% Up", msp: "₹2,300/q", action: "Steady buyer demand in local APMC." },
  "cotton": { name: "Cotton", price: "₹7,420 / q", trend: "📈 +2.4% Up", msp: "₹7,121/q", action: "High mill procurement; good time to sell." },
  "wheat": { name: "Wheat", price: "₹2,480 / q", trend: "📊 Steady", msp: "₹2,275/q", action: "Procurement centers open at MSP." },
  "maize": { name: "Maize (Corn)", price: "₹2,250 / q", trend: "📈 +1.2% Up", msp: "₹2,090/q", action: "Poultry feed demand firming up prices." },
  "chilli": { name: "Chilli", price: "₹18,500 / q", trend: "🔥 High Demand", msp: "Open Market", action: "Export demand strong; premium for dry quality." },
  "soybean": { name: "Soybean", price: "₹4,850 / q", trend: "📊 Stable", msp: "₹4,892/q", action: "Crushing plant demand steady." },
  "groundnut": { name: "Groundnut", price: "₹6,800 / q", trend: "📈 +3.1% Up", msp: "₹6,783/q", action: "Oil expellers buying at premium." },
  "turmeric": { name: "Turmeric", price: "₹14,200 / q", trend: "📈 Rising", msp: "Open Market", action: "Hold dry stock for festival demand." },
  "sugarcane": { name: "Sugarcane", price: "₹340 / q", trend: "📊 Steady", msp: "₹315 FRP", action: "Sugar mills scheduling crushing passes." }
};

export default function DailyBriefing({
  farmer,
  language,
  farmData,
  latestCrop,
  onDataUpdated,
  addToast
}) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const b = t.briefing || TRANSLATIONS.English.briefing;

  // Audio Playback state
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [secondsElapsed, setSecondsElapsed] = useState(0);
  const [speechRate, setSpeechRate] = useState(0.95);
  const [showTranscript, setShowTranscript] = useState(false);

  // Quick Daily Farm Data Update Modal state
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [isSavingData, setIsSavingData] = useState(false);
  const [editTelemetry, setEditTelemetry] = useState({
    nitrogen: farmData?.nitrogen ?? 90,
    phosphorus: farmData?.phosphorus ?? 42,
    potassium: farmData?.potassium ?? 43,
    temperature: farmData?.temperature ?? 28.0,
    humidity: farmData?.humidity ?? 75.0,
    ph: farmData?.ph ?? 6.8,
    soil_moisture: farmData?.soil_moisture ?? 42.0,
    rainfall: farmData?.rainfall ?? 160.0
  });

  // Briefing Data & Script
  const [briefingData, setBriefingData] = useState(null);
  const [loadingBriefing, setLoadingBriefing] = useState(false);

  const synthRef = useRef(typeof window !== 'undefined' ? window.speechSynthesis : null);
  const timerRef = useRef(null);
  const utteranceRef = useRef(null);

  // Load briefing from backend or generate locally
  const fetchBriefing = async () => {
    if (!farmer?.id) return;
    setLoadingBriefing(true);
    try {
      const res = await api.getDailyBriefing(farmer.id, language);
      if (res && res.status === 'success' && res.audio_script) {
        setBriefingData(res);
      } else {
        generateLocalBriefing();
      }
    } catch (e) {
      generateLocalBriefing();
    } finally {
      setLoadingBriefing(false);
    }
  };

  const generateLocalBriefing = () => {
    const farmerName = farmer?.name || 'Farmer';
    const moisture = parseFloat(farmData?.soil_moisture ?? 42);
    const temp = parseFloat(farmData?.temperature ?? 28);
    const ph = parseFloat(farmData?.ph ?? 6.8);
    const cropName = latestCrop?.crop || 'Cotton';
    const cropKey = cropName.toLowerCase().split(' ')[0];
    const mandi = MANDI_RATES_CLIENT[cropKey] || MANDI_RATES_CLIENT['cotton'];
    const needsWater = moisture < 35;
    const todayStr = new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' });

    let script = "";
    if (language === 'తెలుగు') {
      script = `నమస్కారం ${farmerName} గారు! ఇది మీ AgriSense AI నేటి 1 నిమిషం వ్యవసాయ అప్‌డేట్. తేదీ ${todayStr}. మీ పొలంలో తాజా నేల తేమ ${moisture.toFixed(0)} శాతం, ఉష్ణోగ్రత ${temp.toFixed(0)} డిగ్రీలు, నేల pH ${ph.toFixed(1)}. ${needsWater ? 'నేలలో తేమ తక్కువగా ఉంది, ఈరోజు ఉదయాన్నే 2 గంటలు తేలికపాటి తడి అందించండి.' : 'నేలలో తగినంత తేమ ఉంది, ఈరోజు అదనపు నీరు అవసరం లేదు.'} మీ ఎంపిక పంట ${cropName}. నేడు మార్కెట్‌లో ${mandi.name} క్వింటాల్ సగటు ధర ${mandi.price}, ధోరణి ${mandi.trend}. ${mandi.action} పంట ఆరోగ్య సూచన: వాతావరణ తేమ వల్ల తెగుళ్లు రాకుండా లీటరు నీటికి 5 మిల్లీలీటర్ల వేప నూనెను పిచికారీ చేయండి. ప్రభుత్వ పథకం సూచన: పిఎం కిసాన్ మరియు పంటల బీమా ప్రయోజనాలను సద్వినియోగం చేసుకోండి. మంచి దిగుబడి కోసం AgriSense AI శుభాకాంక్షలు!`;
    } else if (language === 'हिंदी') {
      script = `नमस्ते ${farmerName} जी! यह है आपका AgriSense AI दैनिक 1 मिनट का फार्म अपडेट। आज तारीख है ${todayStr}। आपके खेत की मिट्टी में नमी ${moisture.toFixed(0)} प्रतिशत, तापमान ${temp.toFixed(0)} डिग्री और pH ${ph.toFixed(1)} है। ${needsWater ? 'मिट्टी में नमी कम है, इसलिए आज सुबह 2 घंटे हल्की सिंचाई अवश्य करें।' : 'मिट्टी में पर्याप्त नमी बनी हुई है, आज सिंचाई की आवश्यकता नहीं है।'} आपकी चुनी हुई फसल ${cropName} है। आज नजदीकी मंडी में ${mandi.name} का औसत भाव ${mandi.price}, बाजार रुख ${mandi.trend} है। ${mandi.action} फसल स्वास्थ्य निर्देश: फफूंद व कीटों से बचाव हेतु प्रति लीटर पानी में 5 मि.ली. नीम तेल मिलाकर छिड़काव करें। आज की कृषि सलाह: पीएम-किसान व फसल बीमा योजना का लाभ उठाएं। अच्छी पैदावार के लिए शुभकामनाएं!`;
    } else if (language === 'தமிழ்') {
      script = `வணக்கம் ${farmerName}! இது உங்கள் AgriSense AI-ன் இன்றைய 1 நிமிட பண்ணை அறிக்கை. நாள் ${todayStr}. உங்கள் பண்ணை மண் ஈரப்பதம் ${moisture.toFixed(0)}%, வெப்பநிலை ${temp.toFixed(0)} டிகிரி, மண் pH ${ph.toFixed(1)}. ${needsWater ? 'மண்ணில் ஈரப்பதம் குறைவு, இன்று காலை பாசனம் செய்யவும்.' : 'மண்ணில் ஈரப்பதம் சரியாக உள்ளது, இன்று பாசனம் தேவையில்லை.'} பரிந்துரைக்கப்பட்ட பயிர் ${cropName}. இன்றைய சந்தையில் ${mandi.name} குவிண்டால் சராசரி விலை ${mandi.price}, போக்கு ${mandi.trend}. பயிர் பாதுகாப்பு: இலைப்புள்ளி நோயைத் தடுக்க வேப்பெண்ணெய் 5ml/லிட்டர் தெளிக்கவும். உழவன் செயலி மற்றும் பயிர் காப்பீட்டைப் பயன்படுத்தவும்!`;
    } else if (language === 'ಕನ್ನಡ') {
      script = `ನಮಸ್ಕಾರ ${farmerName}! ಇದು ನಿಮ್ಮ AgriSense AI ಇಂದಿನ 1 ನಿಮಿಷದ ಕೃಷಿ ವರದಿ. ದಿನಾಂಕ ${todayStr}. ನಿಮ್ಮ ಜಮೀನಿನ ಮಣ್ಣಿನ ತೇವಾಂಶ ${moisture.toFixed(0)}%, ತಾಪಮಾನ ${temp.toFixed(0)} ಡಿಗ್ರಿ, pH ${ph.toFixed(1)}. ${needsWater ? 'ಮಣ್ಣಿನಲ್ಲಿ ತೇವಾಂಶ ಕಡಿಮೆ ಇದೆ, ಇಂದು ಬೆಳಗ್ಗೆ ನೀರಾವರಿ ಮಾಡಿ.' : 'ಮಣ್ಣಿನಲ್ಲಿ ತೇವಾಂಶ ಉತ್ತಮವಾಗಿದೆ, ಇಂದು ನೀರು ಬೇಡ.'} ಶಿಫಾರಸು ಬೆಳೆ ${cropName}. ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ${mandi.name} ಕ್ವಿಂಟಾಲ್‌ಗೆ ${mandi.price} ಬೆಲೆ ಇದೆ. ರೋಗ ತಡೆಗಟ್ಟಲು ಲೀಟರ್ ನೀರಿಗೆ 5 ಮಿ.ಲೀ ಬೇವಿನ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ. ಕಿಸಾನ್ ಕ್ರೆಡಿಟ್ ಕಾರ್ಡ್ ಸೌಲಭ್ಯವನ್ನು ಪಡೆದುಕೊಳ್ಳಿ!`;
    } else if (language === 'मराठी') {
      script = `नमस्कार ${farmerName}! हे आहे तुमचे AgriSense AI चे आजचे 1 मिनिटांचे कृषी बुलेटीन. तारीख ${todayStr}. शेतातील मातीतील ओलावा ${moisture.toFixed(0)} टक्के, तापमान ${temp.toFixed(0)} अंश सेल्सिअस, pH ${ph.toFixed(1)}. ${needsWater ? 'मातीत ओलावा कमी आहे, आज सकाळी हलके पाणी द्या.' : 'मातीत चांगला ओलावा आहे, आज पाण्याची गरज नाही.'} तुमचे पीक ${cropName}. आजच्या बाजारात ${mandi.name} चा सरासरी भाव ${mandi.price} आहे. कीड नियंत्रणासाठी कडुलिंब तेलाची 5 मिली प्रति लिटर फवारणी करा. पीक विमा योजनेचा लाभ घ्या!`;
    } else {
      script = `Hello ${farmerName}! Here is your AgriSense AI 1-Minute Daily Farm Briefing for ${todayStr}. Your field root-zone soil moisture is ${moisture.toFixed(0)} percent, temperature is ${temp.toFixed(0)} degrees Celsius, and soil pH is ${ph.toFixed(1)}. ${needsWater ? 'Soil moisture is below target, so light irrigation is advised this morning.' : 'Soil moisture is optimal, no irrigation needed today.'} For your selected crop ${cropName}, today's average mandi market rate is ${mandi.price} with a ${mandi.trend} market trend. ${mandi.action} Crop health alert: high atmospheric humidity may trigger leaf spots; spray 5 ml neem oil per litre of water as preventive care. Daily tip: Take advantage of PM-Kisan and PMFBY crop insurance portals. AgriSense AI wishes you a high yield harvest!`;
    }

    setBriefingData({
      status: 'success',
      date: todayStr,
      farmer_name: farmerName,
      language,
      crop: cropName,
      audio_script: script,
      duration_seconds: 60,
      telemetry: {
        soil_moisture: moisture,
        temperature: temp,
        ph,
        nitrogen: farmData?.nitrogen ?? 90,
        phosphorus: farmData?.phosphorus ?? 42,
        potassium: farmData?.potassium ?? 43,
        needs_water: needsWater
      },
      mandi
    });
  };

  useEffect(() => {
    fetchBriefing();
    // Stop audio if language changes
    stopAudio();
  }, [language, farmer?.id, farmData?.soil_moisture, latestCrop?.crop]);

  // Clean up timer on unmount
  useEffect(() => {
    return () => {
      stopAudio();
    };
  }, []);

  // Sync edit modal with farmData
  useEffect(() => {
    if (farmData) {
      setEditTelemetry({
        nitrogen: farmData.nitrogen ?? 90,
        phosphorus: farmData.phosphorus ?? 42,
        potassium: farmData.potassium ?? 43,
        temperature: farmData.temperature ?? 28.0,
        humidity: farmData.humidity ?? 75.0,
        ph: farmData.ph ?? 6.8,
        soil_moisture: farmData.soil_moisture ?? 42.0,
        rainfall: farmData.rainfall ?? 160.0
      });
    }
  }, [farmData]);

  // -------------------------------------------------------------------
  // AUDIO SPEECH PLAYBACK ENGINE
  // -------------------------------------------------------------------
  const langCodeMap = {
    English: 'en-IN',
    'తెలుగు': 'te-IN',
    'हिंदी': 'hi-IN',
    'தமிழ்': 'ta-IN',
    'ಕನ್ನಡ': 'kn-IN',
    'मराठी': 'mr-IN',
  };

  const findBestVoice = (langTag) => {
    if (!synthRef.current) return null;
    const voices = synthRef.current.getVoices() || [];
    const prefix = langTag.split('-')[0].toLowerCase();
    // Exact match first
    let match = voices.find((v) => v.lang.toLowerCase() === langTag.toLowerCase());
    if (match) return match;
    // Prefix match
    match = voices.find((v) => v.lang.toLowerCase().startsWith(prefix));
    if (match) return match;
    // Name match
    match = voices.find((v) => v.name.toLowerCase().includes(prefix));
    return match || null;
  };

  const handlePlayBriefing = () => {
    if (!synthRef.current) {
      if (addToast) addToast('Voice synthesis is not supported on this device/browser', 'error');
      return;
    }

    const script = briefingData?.audio_script;
    if (!script) return;

    if (isPaused) {
      synthRef.current.resume();
      setIsPaused(false);
      setIsPlaying(true);
      startTimer();
      return;
    }

    synthRef.current.cancel();

    const targetLangCode = langCodeMap[language] || 'en-IN';
    const utterance = new SpeechSynthesisUtterance(script);
    utterance.lang = targetLangCode;
    utterance.rate = speechRate;

    const matchedVoice = findBestVoice(targetLangCode);
    if (matchedVoice) {
      utterance.voice = matchedVoice;
    }

    utterance.onstart = () => {
      setIsPlaying(true);
      setIsPaused(false);
      setSecondsElapsed(0);
      startTimer();
    };

    utterance.onend = () => {
      stopAudio();
      setSecondsElapsed(60);
    };

    utterance.onerror = (err) => {
      console.warn('Speech error:', err);
      stopAudio();
    };

    utteranceRef.current = utterance;
    synthRef.current.speak(utterance);
  };

  const handlePauseBriefing = () => {
    if (!synthRef.current) return;
    synthRef.current.pause();
    setIsPaused(true);
    setIsPlaying(false);
    clearInterval(timerRef.current);
  };

  const stopAudio = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
    }
    clearInterval(timerRef.current);
    setIsPlaying(false);
    setIsPaused(false);
    setSecondsElapsed(0);
  };

  const startTimer = () => {
    clearInterval(timerRef.current);
    timerRef.current = setInterval(() => {
      setSecondsElapsed((prev) => {
        if (prev >= 60) {
          clearInterval(timerRef.current);
          return 60;
        }
        return prev + 1;
      });
    }, 1000);
  };

  // -------------------------------------------------------------------
  // SAVE DAILY FARM DATA CHECK-IN
  // -------------------------------------------------------------------
  const handleSaveDailyData = async (e) => {
    e.preventDefault();
    setIsSavingData(true);
    try {
      const payload = {
        farmer_id: farmer?.id || 1,
        nitrogen: parseFloat(editTelemetry.nitrogen),
        phosphorus: parseFloat(editTelemetry.phosphorus),
        potassium: parseFloat(editTelemetry.potassium),
        temperature: parseFloat(editTelemetry.temperature),
        humidity: parseFloat(editTelemetry.humidity),
        ph: parseFloat(editTelemetry.ph),
        soil_moisture: parseFloat(editTelemetry.soil_moisture),
        rainfall: parseFloat(editTelemetry.rainfall),
        source: 'manual'
      };

      const res = await api.saveManualFarmData(payload);
      if (res && res.status === 'success') {
        if (onDataUpdated) onDataUpdated(payload);
        if (addToast) addToast(b.saved || "Today's farm reading updated!", 'success');
        setIsEditModalOpen(false);
        fetchBriefing();
      }
    } catch (err) {
      console.warn('Daily save error:', err);
      if (onDataUpdated) onDataUpdated(editTelemetry);
      if (addToast) addToast(b.saved || "Reading updated locally", 'info');
      setIsEditModalOpen(false);
      generateLocalBriefing();
    } finally {
      setIsSavingData(false);
    }
  };

  const currentCrop = briefingData?.crop || latestCrop?.crop || 'Cotton';
  const currentMandi = briefingData?.mandi || MANDI_RATES_CLIENT['cotton'];
  const telemetry = briefingData?.telemetry || {
    soil_moisture: farmData?.soil_moisture ?? 42,
    temperature: farmData?.temperature ?? 28,
    ph: farmData?.ph ?? 6.8,
    needs_water: (farmData?.soil_moisture ?? 42) < 35
  };

  return (
    <div
      className="agri-card daily-briefing-card"
      style={{
        background: 'linear-gradient(135deg, #064e3b 0%, #065f46 60%, #047857 100%)',
        color: '#ffffff',
        padding: '24px',
        borderRadius: 22,
        boxShadow: '0 10px 30px rgba(6, 78, 59, 0.35)',
        border: '1.5px solid rgba(52, 211, 153, 0.3)',
        position: 'relative',
        overflow: 'hidden'
      }}
    >
      {/* Decorative background glow */}
      <div
        style={{
          position: 'absolute',
          top: -40,
          right: -40,
          width: 180,
          height: 180,
          background: 'radial-gradient(circle, rgba(52,211,153,0.25) 0%, transparent 70%)',
          pointerEvents: 'none'
        }}
      />

      {/* Top Header Row */}
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: 12, marginBottom: 16 }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: 7, background: 'rgba(255,255,255,0.18)', padding: '4px 12px', borderRadius: 99, fontSize: 11.5, fontWeight: 800, letterSpacing: '0.4px', textTransform: 'uppercase', marginBottom: 8, backdropFilter: 'blur(6px)' }}>
            <Sparkles size={12} className="pulse-glow" />
            {b.badge || "Daily 1-Min Audio Briefing"}
          </div>
          <h2 style={{ fontSize: 'clamp(18px, 3.5vw, 24px)', fontWeight: 800, margin: '0 0 4px 0', color: '#ffffff', fontFamily: 'Outfit, sans-serif' }}>
            📻 {b.title || "Today's Farm & Market Intelligence"}
          </h2>
          <p style={{ color: 'rgba(236, 253, 245, 0.88)', fontSize: 13, margin: 0, maxWidth: 620, lineHeight: 1.5 }}>
            {b.subtitle || "1-minute spoken briefing explaining your soil data, selected crop, live market price, and health advice."}
          </p>
        </div>

        {/* Date and Quick Update Button */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 6, background: 'rgba(0,0,0,0.22)', padding: '6px 12px', borderRadius: 12, fontSize: 12, fontWeight: 700, border: '1px solid rgba(255,255,255,0.15)' }}>
            <Calendar size={13} style={{ color: '#6ee7b7' }} />
            <span>{briefingData?.date || new Date().toLocaleDateString('en-GB', { day: 'numeric', month: 'short', year: 'numeric' })}</span>
          </div>

          <button
            onClick={() => setIsEditModalOpen(true)}
            className="btn"
            style={{
              background: '#ffffff',
              color: '#065f46',
              fontWeight: 800,
              fontSize: 12,
              padding: '7px 14px',
              borderRadius: 12,
              boxShadow: '0 4px 12px rgba(0,0,0,0.15)'
            }}
          >
            <Edit3 size={13} />
            <span>{b.updateToday || "Update Today's Data"}</span>
          </button>
        </div>
      </div>

      {/* ── AUDIO PLAYER CONTROLS ── */}
      <div
        style={{
          background: 'rgba(0, 0, 0, 0.28)',
          borderRadius: 18,
          padding: '16px 20px',
          marginBottom: 20,
          border: '1px solid rgba(255, 255, 255, 0.12)',
          display: 'flex',
          flexDirection: 'column',
          gap: 12
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: 14 }}>
          {/* Main Play / Pause Controls */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
            {!isPlaying ? (
              <button
                onClick={handlePlayBriefing}
                className="btn"
                style={{
                  background: 'linear-gradient(135deg, #10b981 0%, #059669 100%)',
                  color: '#ffffff',
                  fontSize: 14,
                  fontWeight: 800,
                  padding: '10px 22px',
                  borderRadius: 14,
                  boxShadow: '0 6px 16px rgba(16, 185, 129, 0.45)',
                  minHeight: 46
                }}
              >
                <Play size={16} fill="white" />
                <span>{b.play || "▶️ Play 1-Min Briefing"}</span>
              </button>
            ) : (
              <div style={{ display: 'flex', gap: 8 }}>
                <button
                  onClick={handlePauseBriefing}
                  className="btn"
                  style={{
                    background: '#fbbf24',
                    color: '#78350f',
                    fontWeight: 800,
                    padding: '10px 18px',
                    borderRadius: 14,
                    minHeight: 46
                  }}
                >
                  <Pause size={16} fill="#78350f" />
                  <span>{b.pause || "Pause"}</span>
                </button>
                <button
                  onClick={stopAudio}
                  className="btn"
                  style={{
                    background: 'rgba(239, 68, 68, 0.9)',
                    color: '#ffffff',
                    fontWeight: 800,
                    padding: '10px 16px',
                    borderRadius: 14,
                    minHeight: 46
                  }}
                >
                  <Square size={15} fill="white" />
                  <span>{b.stop || "Stop"}</span>
                </button>
              </div>
            )}

            {/* Speaking animation / status */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              {isPlaying && (
                <div style={{ display: 'flex', alignItems: 'flex-end', gap: 3, height: 20 }}>
                  <span className="sound-wave-bar" style={{ animationDelay: '0.1s' }} />
                  <span className="sound-wave-bar" style={{ animationDelay: '0.3s' }} />
                  <span className="sound-wave-bar" style={{ animationDelay: '0.2s' }} />
                  <span className="sound-wave-bar" style={{ animationDelay: '0.4s' }} />
                  <span className="sound-wave-bar" style={{ animationDelay: '0.15s' }} />
                </div>
              )}
              <span style={{ fontSize: 13, fontWeight: 700, color: isPlaying ? '#a7f3d0' : '#e2e8f0' }}>
                {isPlaying
                  ? `${b.playing || "AgriSense AI Speaking in"} ${language}...`
                  : isPaused
                  ? "⏸ Paused"
                  : `🗣️ Voice: ${language}`}
              </span>
            </div>
          </div>

          {/* Timer & Speech Speed Selector */}
          <div style={{ display: 'flex', alignItems: 'center', gap: 14 }}>
            {/* Progress Timer */}
            <div style={{ display: 'flex', alignItems: 'center', gap: 6, fontSize: 13, fontWeight: 800, color: '#6ee7b7' }}>
              <Clock size={14} />
              <span>0:{secondsElapsed.toString().padStart(2, '0')} / 1:00</span>
            </div>

            {/* Speed pills */}
            <div style={{ display: 'flex', alignItems: 'center', background: 'rgba(255,255,255,0.12)', borderRadius: 10, padding: 2 }}>
              {[0.85, 1.0, 1.15].map((rate) => (
                <button
                  key={rate}
                  onClick={() => setSpeechRate(rate)}
                  style={{
                    background: speechRate === rate ? '#ffffff' : 'transparent',
                    color: speechRate === rate ? '#065f46' : 'rgba(255,255,255,0.85)',
                    border: 'none',
                    borderRadius: 8,
                    padding: '4px 8px',
                    fontSize: 11,
                    fontWeight: 800,
                    cursor: 'pointer'
                  }}
                >
                  {rate}x
                </button>
              ))}
            </div>

            {/* Transcript Toggle */}
            <button
              onClick={() => setShowTranscript(!showTranscript)}
              style={{
                background: 'transparent',
                border: '1px solid rgba(255,255,255,0.25)',
                color: '#ffffff',
                borderRadius: 10,
                padding: '5px 10px',
                fontSize: 11.5,
                fontWeight: 700,
                cursor: 'pointer',
                display: 'flex',
                alignItems: 'center',
                gap: 5
              }}
            >
              <span>{b.transcriptTitle || "Transcript"}</span>
              {showTranscript ? <ChevronUp size={13} /> : <ChevronDown size={13} />}
            </button>
          </div>
        </div>

        {/* 60s Progress Bar */}
        <div style={{ width: '100%', height: 6, background: 'rgba(255,255,255,0.15)', borderRadius: 99, overflow: 'hidden' }}>
          <div
            style={{
              height: '100%',
              width: `${Math.min(100, (secondsElapsed / 60) * 100)}%`,
              background: 'linear-gradient(90deg, #34d399, #10b981)',
              borderRadius: 99,
              transition: 'width 1s linear'
            }}
          />
        </div>
      </div>

      {/* ── 4 QUICK INTELLIGENCE CARDS (RESPONSIVE GRID) ── */}
      <div
        style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 200px), 1fr))',
          gap: 12,
          marginBottom: showTranscript ? 16 : 0
        }}
      >
        {/* Card 1: Selected Crop */}
        <div
          style={{
            background: 'rgba(255, 255, 255, 0.08)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: 16,
            padding: '14px 16px',
            backdropFilter: 'blur(8px)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 6 }}>
            <div style={{ background: '#ecfdf5', color: '#047857', padding: 5, borderRadius: 8 }}>
              <Wheat size={15} />
            </div>
            <span style={{ fontSize: 11.5, fontWeight: 700, textTransform: 'uppercase', color: '#a7f3d0' }}>
              {b.cropCardTitle || "Selected Crop"}
            </span>
          </div>
          <div style={{ fontSize: 17, fontWeight: 800, color: '#ffffff', marginBottom: 2 }}>
            {currentCrop}
          </div>
          <div style={{ fontSize: 11.5, color: '#d1fae5', lineHeight: 1.4 }}>
            {telemetry.needs_water
              ? "💧 Irrigation needed: Apply morning watering"
              : "✅ Soil moisture optimal (42%)"}
          </div>
        </div>

        {/* Card 2: Today's Mandi Price */}
        <div
          style={{
            background: 'rgba(255, 255, 255, 0.08)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: 16,
            padding: '14px 16px',
            backdropFilter: 'blur(8px)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 6 }}>
            <div style={{ background: '#f5f3ff', color: '#6d28d9', padding: 5, borderRadius: 8 }}>
              <TrendingUp size={15} />
            </div>
            <span style={{ fontSize: 11.5, fontWeight: 700, textTransform: 'uppercase', color: '#c4b5fd' }}>
              {b.mandiCardTitle || "Today's Mandi Price"}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'baseline', gap: 8, marginBottom: 2 }}>
            <span style={{ fontSize: 17, fontWeight: 800, color: '#ffffff' }}>
              {currentMandi.price}
            </span>
            <span style={{ fontSize: 11, fontWeight: 700, color: '#fef08a' }}>
              {currentMandi.trend}
            </span>
          </div>
          <div style={{ fontSize: 11.5, color: '#ede9fe', lineHeight: 1.4 }}>
            MSP: {currentMandi.msp} • Local APMC rate
          </div>
        </div>

        {/* Card 3: Crop Health & Protection */}
        <div
          style={{
            background: 'rgba(255, 255, 255, 0.08)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: 16,
            padding: '14px 16px',
            backdropFilter: 'blur(8px)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 6 }}>
            <div style={{ background: '#fef2f2', color: '#b91c1c', padding: 5, borderRadius: 8 }}>
              <ShieldAlert size={15} />
            </div>
            <span style={{ fontSize: 11.5, fontWeight: 700, textTransform: 'uppercase', color: '#fca5a5' }}>
              {b.healthCardTitle || "Health & Protection"}
            </span>
          </div>
          <div style={{ fontSize: 13.5, fontWeight: 800, color: '#ffffff', marginBottom: 2 }}>
            Pest & Fungal Alert
          </div>
          <div style={{ fontSize: 11.5, color: '#fee2e2', lineHeight: 1.4 }}>
            Spray Neem Oil 5ml/L preventively in morning hours.
          </div>
        </div>

        {/* Card 4: Tip of the Day */}
        <div
          style={{
            background: 'rgba(255, 255, 255, 0.08)',
            border: '1px solid rgba(255, 255, 255, 0.15)',
            borderRadius: 16,
            padding: '14px 16px',
            backdropFilter: 'blur(8px)'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: 7, marginBottom: 6 }}>
            <div style={{ background: '#fffbeb', color: '#b45309', padding: 5, borderRadius: 8 }}>
              <Lightbulb size={15} />
            </div>
            <span style={{ fontSize: 11.5, fontWeight: 700, textTransform: 'uppercase', color: '#fde68a' }}>
              {b.tipCardTitle || "Tip of the Day"}
            </span>
          </div>
          <div style={{ fontSize: 13.5, fontWeight: 800, color: '#ffffff', marginBottom: 2 }}>
            Govt Subsidies
          </div>
          <div style={{ fontSize: 11.5, color: '#fef3c7', lineHeight: 1.4 }}>
            PM-Kisan & PMFBY insurance enrollment active in portal.
          </div>
        </div>
      </div>

      {/* ── EXPANDABLE SPOKEN TRANSCRIPT IN FARMER'S LANGUAGE ── */}
      {showTranscript && (
        <div
          style={{
            background: 'rgba(0,0,0,0.32)',
            borderRadius: 16,
            padding: '16px 20px',
            border: '1px solid rgba(255,255,255,0.15)',
            marginTop: 14
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 8 }}>
            <span style={{ fontSize: 12.5, fontWeight: 800, color: '#6ee7b7' }}>
              📜 {b.transcriptTitle || "1-Minute Spoken Transcript"} ({language})
            </span>
            <button
              onClick={handlePlayBriefing}
              style={{
                background: 'rgba(255,255,255,0.18)',
                color: '#ffffff',
                border: 'none',
                borderRadius: 8,
                padding: '4px 10px',
                fontSize: 11,
                fontWeight: 700,
                cursor: 'pointer'
              }}
            >
              🔊 {b.play || "Listen"}
            </button>
          </div>
          <p style={{ margin: 0, fontSize: 13.5, lineHeight: 1.6, color: '#f0fdf4', whiteSpace: 'pre-line' }}>
            {briefingData?.audio_script}
          </p>
        </div>
      )}

      {/* ── MODAL: QUICK DAILY FARM DATA UPDATE ── */}
      {isEditModalOpen && (
        <div
          style={{
            position: 'fixed',
            inset: 0,
            zIndex: 1000,
            background: 'rgba(0,0,0,0.65)',
            backdropFilter: 'blur(8px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: 16
          }}
        >
          <div
            className="agri-card"
            style={{
              background: '#ffffff',
              color: '#0f172a',
              width: '100%',
              maxWidth: 520,
              borderRadius: 22,
              padding: '24px',
              boxShadow: '0 20px 45px rgba(0,0,0,0.3)',
              maxHeight: '90vh',
              overflowY: 'auto'
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
              <div>
                <h3 style={{ margin: '0 0 4px 0', fontSize: 20, fontWeight: 800, color: '#065f46' }}>
                  📝 {b.quickCheckin || "Quick Daily Farm Check-In"}
                </h3>
                <p style={{ margin: 0, fontSize: 12.5, color: '#64748b' }}>
                  Update today's readings so your 1-minute briefing and crop advice refresh.
                </p>
              </div>
              <button
                onClick={() => setIsEditModalOpen(false)}
                style={{ background: '#f1f5f9', border: 'none', borderRadius: 99, padding: 6, cursor: 'pointer' }}
              >
                <X size={18} color="#475569" />
              </button>
            </div>

            <form onSubmit={handleSaveDailyData} style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              {/* Soil Moisture Slider */}
              <div style={{ background: '#f0fdf4', padding: '12px 16px', borderRadius: 14, border: '1px solid #bbf7d0' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                  <label style={{ fontSize: 13, fontWeight: 800, color: '#166534' }}>
                    💧 Root-Zone Soil Moisture
                  </label>
                  <span style={{ fontSize: 14, fontWeight: 800, color: '#15803d' }}>
                    {editTelemetry.soil_moisture}%
                  </span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="90"
                  value={editTelemetry.soil_moisture}
                  onChange={(e) => setEditTelemetry({ ...editTelemetry, soil_moisture: parseFloat(e.target.value) })}
                  style={{ width: '100%', cursor: 'pointer' }}
                />
                <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 10.5, color: '#64748b', marginTop: 2 }}>
                  <span>Dry (&lt;30%)</span>
                  <span>Optimal (35-55%)</span>
                  <span>Wet (&gt;60%)</span>
                </div>
              </div>

              {/* Temp and Humidity */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 140px), 1fr))', gap: 12 }}>
                <div>
                  <label style={{ fontSize: 12, fontWeight: 700, color: '#334155', display: 'block', marginBottom: 4 }}>
                    🌡️ Temperature (°C)
                  </label>
                  <input
                    type="number"
                    step="0.5"
                    value={editTelemetry.temperature}
                    onChange={(e) => setEditTelemetry({ ...editTelemetry, temperature: parseFloat(e.target.value) || 25 })}
                    className="input-field"
                    style={{ height: 42, fontSize: 14 }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: 12, fontWeight: 700, color: '#334155', display: 'block', marginBottom: 4 }}>
                    🌫️ Humidity (%)
                  </label>
                  <input
                    type="number"
                    step="1"
                    value={editTelemetry.humidity}
                    onChange={(e) => setEditTelemetry({ ...editTelemetry, humidity: parseFloat(e.target.value) || 70 })}
                    className="input-field"
                    style={{ height: 42, fontSize: 14 }}
                  />
                </div>
              </div>

              {/* N-P-K Readings */}
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(min(100%, 90px), 1fr))', gap: 10 }}>
                <div>
                  <label style={{ fontSize: 11.5, fontWeight: 700, color: '#334155', display: 'block', marginBottom: 4 }}>
                    Nitrogen (N)
                  </label>
                  <input
                    type="number"
                    value={editTelemetry.nitrogen}
                    onChange={(e) => setEditTelemetry({ ...editTelemetry, nitrogen: parseFloat(e.target.value) || 0 })}
                    className="input-field"
                    style={{ height: 42, fontSize: 13 }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: 11.5, fontWeight: 700, color: '#334155', display: 'block', marginBottom: 4 }}>
                    Phosphorus (P)
                  </label>
                  <input
                    type="number"
                    value={editTelemetry.phosphorus}
                    onChange={(e) => setEditTelemetry({ ...editTelemetry, phosphorus: parseFloat(e.target.value) || 0 })}
                    className="input-field"
                    style={{ height: 42, fontSize: 13 }}
                  />
                </div>
                <div>
                  <label style={{ fontSize: 11.5, fontWeight: 700, color: '#334155', display: 'block', marginBottom: 4 }}>
                    Potassium (K)
                  </label>
                  <input
                    type="number"
                    value={editTelemetry.potassium}
                    onChange={(e) => setEditTelemetry({ ...editTelemetry, potassium: parseFloat(e.target.value) || 0 })}
                    className="input-field"
                    style={{ height: 42, fontSize: 13 }}
                  />
                </div>
              </div>

              {/* pH Level */}
              <div>
                <label style={{ fontSize: 12, fontWeight: 700, color: '#334155', display: 'block', marginBottom: 4 }}>
                  🧪 Soil pH (Acidity / Alkalinity)
                </label>
                <input
                  type="number"
                  step="0.1"
                  value={editTelemetry.ph}
                  onChange={(e) => setEditTelemetry({ ...editTelemetry, ph: parseFloat(e.target.value) || 6.5 })}
                  className="input-field"
                  style={{ height: 42, fontSize: 14 }}
                />
              </div>

              {/* Buttons */}
              <div style={{ display: 'flex', gap: 10, marginTop: 8 }}>
                <button
                  type="button"
                  onClick={() => setIsEditModalOpen(false)}
                  className="btn btn-secondary"
                  style={{ flex: 1, height: 46 }}
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={isSavingData}
                  className="btn btn-primary"
                  style={{ flex: 2, height: 46 }}
                >
                  <Save size={15} />
                  <span>{isSavingData ? (b.saving || "Saving...") : (b.saveTodayBtn || "Save Today's Reading")}</span>
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
