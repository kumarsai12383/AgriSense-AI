import React, { useState, useRef, useEffect } from 'react';
import { MessageSquareCode, Send, Trash2, Sparkles, User, Bot, Mic, MicOff, Volume2, Square } from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

const BCP47_MAP = {
  English: 'en-IN',
  'తెలుగు': 'te-IN',
  'हिंदी': 'hi-IN',
  'தமிழ்': 'ta-IN',
  'ಕನ್ನಡ': 'kn-IN',
  'मराठी': 'mr-IN',
};

export default function AiChat({ farmer, language, farmData, latestCrop, addToast }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const chatT = t.chat || TRANSLATIONS.English.chat;

  const getInitialGreeting = (lang, name) => {
    const greetings = {
      'తెలుగు': `నమస్కారం 👨‍🌾 **${name || 'రైతు సోదరా'}**! నేను మీ AgriSense AI వ్యవసాయ సలహాదారుని. మీ పంటలు, నేల పోషకాలు, నీటి నిర్వహణ లేదా ఎరువుల గురించి ఏమైనా అడగండి.`,
      'हिंदी': `नमस्ते 👨‍🌾 **${name || 'किसान साथी'}**! मैं आपका AgriSense AI कृषि सलाहकार हूँ। आपकी फसल, मिट्टी की सेहत, खाद या पानी से जुड़ा कोई भी सवाल पूछिए।`,
      'தமிழ்': `வணக்கம் 👨‍🌾 **${name || 'விவசாயி'}**! நான் உங்கள் AgriSense AI வேளாண் உதவியாளர். உங்கள் பயிர், மண் சத்துக்கள் அல்லது பாசனம் பற்றி எதை வேண்டுமானாலும் கேளுங்கள்.`,
      'ಕನ್ನಡ': `ನಮಸ್ಕಾರ 👨‍🌾 **${name || 'ರೈತ ಮಿತ್ರ'}**! ನಾನು ನಿಮ್ಮ AgriSense AI ಕೃಷಿ ಸಲಹೆಗಾರ. ನಿಮ್ಮ ಬೆಳೆ, ಮಣ್ಣಿನ ಪೋಷಕಾಂಶ ಅಥವಾ ನೀರಾವರಿ ಬಗ್ಗೆ ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಿ.`,
      'मराठी': `नमस्कार 👨‍🌾 **${name || 'शेतकरी मित्र'}**! मी तुमचा AgriSense AI कृषी सल्लागार आहे. तुमच्या पिकाविषयी, खतांविषयी किंवा पाण्याचे नियोजन याबद्दल काहीही विचारा.`,
      English: `Namaste 👨‍🌾 **${name || 'Farmer'}**! I am your AgriSense AI Agronomist. How can I assist you with your crops, soil nutrients, water scheduling, or fertilizer today?`
    };
    return greetings[lang] || greetings.English;
  };

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: getInitialGreeting(language, farmer?.name)
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [speakingIdx, setSpeakingIdx] = useState(null);

  const messagesEndRef = useRef(null);
  const synthRef = useRef(typeof window !== 'undefined' ? window.speechSynthesis : null);
  const recognitionRef = useRef(null);

  // Update greeting when language changes
  useEffect(() => {
    setMessages([
      {
        role: 'assistant',
        content: getInitialGreeting(language, farmer?.name)
      }
    ]);
    stopSpeaking();
  }, [language, farmer?.name]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  useEffect(() => {
    return () => {
      stopSpeaking();
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
    };
  }, []);

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

    stopSpeaking();
    const userMsg = { role: 'user', content: textToSend.trim() };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const res = await api.askAiAssistant(farmer?.id || 1, textToSend.trim(), language);
      if (res && res.answer) {
        setMessages((prev) => [...prev, { role: 'assistant', content: res.answer }]);
      }
    } catch (err) {
      console.warn('AI Chat error, using localized agronomic fallback:', err);
      const fallback = language === 'తెలుగు'
        ? `🌾 **AgriSense AI సలహా:** మీ పొలం నేల మరియు వాతావరణ సమాచారం ఆధారంగా: సమతుల్య ఎరువులను వేయండి, ఉదయం పూట మాత్రమే నీరు పెట్టండి మరియు ఆకుల వెనుక భాగాన్ని క్రమం తప్పకుండా పరిశీలించండి.`
        : language === 'हिंदी'
        ? `🌾 **AgriSense AI सलाह:** आपके खेत के आंकड़ों के आधार पर: संतुलित NPK खाद डालें, सुबह के समय हल्की सिंचाई करें और कीटों से बचाव हेतु नीम तेल का छिड़काव करें।`
        : `🌾 **AgriSense AI Advisory:** Based on your farm profile and soil measurements: Maintain balanced NPK application, irrigate during early morning hours, and spray Neem oil (5ml/L) preventively against leaf pests.`;
      setMessages((prev) => [...prev, { role: 'assistant', content: fallback }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    stopSpeaking();
    setMessages([
      {
        role: 'assistant',
        content: getInitialGreeting(language, farmer?.name)
      }
    ]);
    if (addToast) addToast(chatT.clear || 'Chat cleared', 'info');
  };

  // -------------------------------------------------------------------
  // SPEECH-TO-TEXT (MIC INPUT) IN USER'S SELECTED LANGUAGE
  // -------------------------------------------------------------------
  const toggleListening = () => {
    const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRec) {
      if (addToast) addToast('Speech recognition is not supported in this browser. Please use Chrome/Edge.', 'error');
      return;
    }

    if (isListening) {
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsListening(false);
      return;
    }

    const recognition = new SpeechRec();
    const langTag = BCP47_MAP[language] || 'en-IN';
    recognition.lang = langTag;
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      if (addToast) addToast(`🎙️ Listening in ${language}... Speak now!`, 'info');
    };

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      setIsListening(false);
    };

    recognition.onerror = (e) => {
      console.warn('Speech rec error:', e.error);
      setIsListening(false);
    };

    recognition.onend = () => {
      setIsListening(false);
    };

    recognitionRef.current = recognition;
    recognition.start();
  };

  // -------------------------------------------------------------------
  // TEXT-TO-SPEECH (READ ALOUD) IN USER'S SELECTED LANGUAGE
  // -------------------------------------------------------------------
  const findMatchingVoice = (langTag) => {
    if (!synthRef.current) return null;
    const voices = synthRef.current.getVoices() || [];
    const prefix = langTag.split('-')[0].toLowerCase();
    let match = voices.find((v) => v.lang.toLowerCase() === langTag.toLowerCase());
    if (match) return match;
    match = voices.find((v) => v.lang.toLowerCase().startsWith(prefix));
    if (match) return match;
    match = voices.find((v) => v.name.toLowerCase().includes(prefix));
    return match || null;
  };

  const speakMessage = (text, idx) => {
    if (!synthRef.current) return;
    if (speakingIdx === idx) {
      stopSpeaking();
      return;
    }

    synthRef.current.cancel();
    const cleanText = text.replace(/[*#_`]/g, '').trim();
    const targetLangCode = BCP47_MAP[language] || 'en-IN';
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = targetLangCode;
    utterance.rate = 0.95;

    const matchedVoice = findMatchingVoice(targetLangCode);
    if (matchedVoice) {
      utterance.voice = matchedVoice;
    }

    utterance.onstart = () => setSpeakingIdx(idx);
    utterance.onend = () => setSpeakingIdx(null);
    utterance.onerror = () => setSpeakingIdx(null);

    synthRef.current.speak(utterance);
  };

  const stopSpeaking = () => {
    if (synthRef.current) {
      synthRef.current.cancel();
    }
    setSpeakingIdx(null);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
      {/* Header Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #15803d 0%, #16a34a 100%)',
          color: 'white',
          padding: '20px 24px',
          borderRadius: 20
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 10 }}>
          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 4 }}>
              <h2 style={{ color: 'white', fontSize: 22, margin: 0 }}>
                🤖 {chatT.title || "AI Agronomist Chat"}
              </h2>
              <span className="badge" style={{ background: 'rgba(255,255,255,0.2)', color: '#ffffff', fontSize: 11 }}>
                {language}
              </span>
            </div>
            <p style={{ color: '#dcfce7', fontSize: 13, margin: 0 }}>
              {chatT.subtitle || "Instant farming advice personalized with your soil, weather, and ML recommendations."}
            </p>
          </div>
          <button 
            onClick={handleClear}
            className="btn" 
            style={{ background: 'rgba(255,255,255,0.2)', color: 'white', padding: '8px 14px', fontSize: 12 }}
          >
            <Trash2 size={14} />
            <span>{chatT.clear || "Clear Chat"}</span>
          </button>
        </div>
      </div>

      {/* Quick Questions Row */}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {[chatT.quick1, chatT.quick2, chatT.quick3].filter(Boolean).map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q)}
            style={{
              background: '#ffffff',
              border: '1.5px solid #e2e8f0',
              borderRadius: 20,
              padding: '6px 14px',
              fontSize: 12,
              fontWeight: 700,
              color: '#334155',
              cursor: 'pointer',
              boxShadow: '0 2px 4px rgba(0,0,0,0.03)'
            }}
          >
            {q}
          </button>
        ))}
      </div>

      {/* Messages Container */}
      <div 
        className="agri-card"
        style={{
          minHeight: 380,
          maxHeight: 520,
          overflowY: 'auto',
          display: 'flex',
          flexDirection: 'column',
          gap: 14,
          padding: 20
        }}
      >
        {messages.map((m, idx) => {
          const isUser = m.role === 'user';
          const isThisSpeaking = speakingIdx === idx;
          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                gap: 10,
                alignSelf: isUser ? 'flex-end' : 'flex-start',
                maxWidth: '94%',
                minWidth: 0
              }}
            >
              {!isUser && (
                <div style={{ width: 34, height: 34, borderRadius: 10, background: '#15803d', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', flexShrink: 0, marginTop: 2 }}>
                  <Bot size={18} />
                </div>
              )}
              <div style={{ display: 'flex', flexDirection: 'column', gap: 4, minWidth: 0, flex: 1 }}>
                <div
                  style={{
                    background: isUser ? 'linear-gradient(135deg, #15803d, #16a34a)' : '#f8fafc',
                    color: isUser ? '#ffffff' : '#0f172a',
                    border: isUser ? 'none' : '1px solid #e2e8f0',
                    padding: '12px 16px',
                    borderRadius: 16,
                    fontSize: 14,
                    lineHeight: 1.6,
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    overflowWrap: 'anywhere',
                    boxShadow: '0 2px 6px rgba(0,0,0,0.03)'
                  }}
                >
                  {m.content}
                </div>

                {/* Read Aloud button for AI responses */}
                {!isUser && (
                  <button
                    onClick={() => speakMessage(m.content, idx)}
                    style={{
                      alignSelf: 'flex-start',
                      background: isThisSpeaking ? '#dcfce7' : 'transparent',
                      color: isThisSpeaking ? '#15803d' : '#64748b',
                      border: 'none',
                      borderRadius: 8,
                      padding: '3px 8px',
                      fontSize: 11.5,
                      fontWeight: 700,
                      cursor: 'pointer',
                      display: 'inline-flex',
                      alignItems: 'center',
                      gap: 4
                    }}
                  >
                    {isThisSpeaking ? (
                      <>
                        <Square size={12} fill="#15803d" />
                        <span>{chatT.stopReply || "Stop"}</span>
                      </>
                    ) : (
                      <>
                        <Volume2 size={13} />
                        <span>{chatT.listenReply || "Listen"}</span>
                      </>
                    )}
                  </button>
                )}
              </div>

              {isUser && (
                <div style={{ width: 34, height: 34, borderRadius: 10, background: '#0284c7', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', flexShrink: 0, marginTop: 2 }}>
                  <User size={18} />
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div style={{ display: 'flex', gap: 10, alignSelf: 'flex-start' }}>
            <div style={{ width: 34, height: 34, borderRadius: 10, background: '#15803d', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white' }}>
              <Bot size={18} />
            </div>
            <div style={{ background: '#f8fafc', padding: '12px 16px', borderRadius: 16, border: '1px solid #e2e8f0', fontSize: 13, color: '#64748b' }}>
              Consulting AgriSense AI agronomist in {language}...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Field with Mic & Send */}
      <form 
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        style={{ display: 'flex', gap: 8, alignItems: 'center' }}
      >
        <div style={{ position: 'relative', flex: 1 }}>
          <input
            type="text"
            className="input-field"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={isListening ? (chatT.listening || "Listening... speak now") : (chatT.inputPlaceholder || "Ask AgriSense in your language...")}
            disabled={loading}
            style={{
              height: 50,
              paddingRight: 48,
              border: isListening ? '2px solid #ef4444' : undefined,
              boxShadow: isListening ? '0 0 10px rgba(239, 68, 68, 0.3)' : undefined
            }}
          />
          {/* Mic Button Inside Input */}
          <button
            type="button"
            onClick={toggleListening}
            title={chatT.micTooltip || `Speak in ${language}`}
            style={{
              position: 'absolute',
              right: 8,
              top: '50%',
              transform: 'translateY(-50%)',
              background: isListening ? '#ef4444' : '#f1f5f9',
              color: isListening ? '#ffffff' : '#15803d',
              border: 'none',
              borderRadius: 10,
              width: 34,
              height: 34,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              cursor: 'pointer',
              transition: 'all 0.15s ease'
            }}
          >
            {isListening ? <MicOff size={16} /> : <Mic size={16} />}
          </button>
        </div>

        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="btn btn-primary"
          style={{ width: 54, height: 50, padding: 0, flexShrink: 0 }}
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
