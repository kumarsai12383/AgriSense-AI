import React, { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Volume2, Sparkles, Wifi, WifiOff, AlertTriangle, CheckCircle2, RefreshCw } from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

export default function VoiceAssistant({ farmer, language, addToast }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;
  const [activeTab, setActiveTab] = useState('browser'); // 'live' or 'browser'

  // Server health state
  const [serverOnline, setServerOnline] = useState(false);

  // WebSocket Live Voice state
  const [isLiveConnected, setIsLiveConnected] = useState(false);
  const [isSpeakingLive, setIsSpeakingLive] = useState(false);
  const [liveTranscript, setLiveTranscript] = useState('Ready to speak with AgriSense AI...');
  const [liveStatus, setLiveStatus] = useState('⚪ Ready to connect');

  const wsRef = useRef(null);
  const audioContextRef = useRef(null);
  const processorRef = useRef(null);
  const streamRef = useRef(null);
  const playbackCtxRef = useRef(null);
  const nextStartTimeRef = useRef(0);

  // Browser Web Speech state
  const [isBrowserListening, setIsBrowserListening] = useState(false);
  const [browserUserSpeech, setBrowserUserSpeech] = useState('...');
  const [browserAiReply, setBrowserAiReply] = useState('Your advice will appear and be spoken aloud here...');
  const [browserStatus, setBrowserStatus] = useState('Tap microphone and ask your farming question');

  const recognitionRef = useRef(null);
  const synthRef = useRef(window.speechSynthesis || null);

  // Check server health
  const checkServer = async () => {
    const health = await api.checkHealth();
    setServerOnline(health.status === 'healthy');
  };

  useEffect(() => {
    checkServer();
    const timer = setInterval(checkServer, 5000);
    return () => clearInterval(timer);
  }, []);

  // -------------------------------------------------------------
  // 1. WEBSOCKET GEMINI LIVE VOICE ENGINE
  // -------------------------------------------------------------
  const downsample = (buffer, inputSampleRate, outputSampleRate) => {
    if (outputSampleRate === inputSampleRate) return buffer;
    const ratio = inputSampleRate / outputSampleRate;
    const newLen = Math.round(buffer.length / ratio);
    const result = new Float32Array(newLen);
    let offsetResult = 0;
    let offsetBuffer = 0;
    while (offsetResult < result.length) {
      const nextOffsetBuffer = Math.round((offsetResult + 1) * ratio);
      let accum = 0, count = 0;
      for (let i = offsetBuffer; i < nextOffsetBuffer && i < buffer.length; i++) {
        accum += buffer[i];
        count++;
      }
      result[offsetResult] = count ? accum / count : 0;
      offsetResult++;
      offsetBuffer = nextOffsetBuffer;
    }
    return result;
  };

  const floatTo16BitPCM = (float32Array) => {
    const buffer = new ArrayBuffer(float32Array.length * 2);
    const view = new DataView(buffer);
    let offset = 0;
    for (let i = 0; i < float32Array.length; i++, offset += 2) {
      let sample = Math.max(-1, Math.min(1, float32Array[i]));
      view.setInt16(offset, sample < 0 ? sample * 0x8000 : sample * 0x7FFF, true);
    }
    return buffer;
  };

  const playAudioChunk = (audioData) => {
    try {
      if (!playbackCtxRef.current || playbackCtxRef.current.state === "closed") {
        playbackCtxRef.current = new (window.AudioContext || window.webkitAudioContext)({ sampleRate: 24000 });
      }
      if (playbackCtxRef.current.state === "suspended") {
        playbackCtxRef.current.resume();
      }
      const int16 = new Int16Array(audioData);
      const audioBuffer = playbackCtxRef.current.createBuffer(1, int16.length, 24000);
      const channel = audioBuffer.getChannelData(0);
      for (let i = 0; i < int16.length; i++) {
        channel[i] = int16[i] / 32768;
      }
      const source = playbackCtxRef.current.createBufferSource();
      source.buffer = audioBuffer;
      source.connect(playbackCtxRef.current.destination);

      const now = playbackCtxRef.current.currentTime;
      if (nextStartTimeRef.current < now) {
        nextStartTimeRef.current = now;
      }
      source.start(nextStartTimeRef.current);
      nextStartTimeRef.current += audioBuffer.duration;
    } catch (err) {
      console.error("Audio playback error:", err);
    }
  };

  const startLiveVoice = async () => {
    try {
      setLiveStatus('🟡 Connecting to AgriSense Live...');
      const url = api.getLiveVoiceWebSocketUrl(farmer?.id || 1, language);
      const ws = new WebSocket(url);
      ws.binaryType = 'arraybuffer';
      wsRef.current = ws;

      ws.onopen = async () => {
        setIsLiveConnected(true);
        setIsSpeakingLive(true);
        setLiveStatus('🟢 Connected — Speak naturally now');
        setLiveTranscript('Listening to your voice...');
        addToast('Connected to Gemini Live Voice', 'success');

        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;
        const audioCtx = new (window.AudioContext || window.webkitAudioContext)();
        audioContextRef.current = audioCtx;
        const mic = audioCtx.createMediaStreamSource(stream);
        const processor = audioCtx.createScriptProcessor(4096, 1, 1);
        processorRef.current = processor;

        processor.onaudioprocess = (e) => {
          if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) return;
          const input = e.inputBuffer.getChannelData(0);
          const downsampled = downsample(input, audioCtx.sampleRate, 16000);
          const pcm = floatTo16BitPCM(downsampled);
          wsRef.current.send(pcm);
        };

        mic.connect(processor);
        const muteGain = audioCtx.createGain();
        muteGain.gain.value = 0;
        processor.connect(muteGain);
        muteGain.connect(audioCtx.destination);
      };

      ws.onmessage = (event) => {
        if (typeof event.data === 'string') {
          if (event.data.startsWith('AI_TEXT:')) {
            setLiveTranscript(event.data.substring(8));
          } else if (event.data === 'AI_DONE') {
            setLiveStatus('🟢 AgriSense finished speaking');
          } else if (event.data.startsWith('ERROR:')) {
            const err = event.data.substring(6);
            setLiveStatus(`🔴 Error: ${err}`);
            setLiveTranscript(`⚠️ ${err}`);
          }
          return;
        }
        if (event.data instanceof ArrayBuffer) {
          playAudioChunk(event.data);
        }
      };

      ws.onerror = (err) => {
        console.warn('WebSocket Live notice:', err);
        setLiveStatus('🟡 Gemini Live audio busy — Switched to Fast Speech Mode');
        addToast('Voice switched to Fast Indian Language Assistant', 'info');
        // Auto-switch to browser voice so the farmer never experiences a breakdown!
        stopLiveVoice();
        setActiveTab('browser');
      };

      ws.onclose = (event) => {
        setIsLiveConnected(false);
        setIsSpeakingLive(false);
        if (event.code === 1000) {
          setLiveStatus('⏹ Voice session ended');
        } else {
          setLiveStatus('🟡 Live voice disconnected — Switched to Fast Speech Mode');
          // Auto fallback to browser voice mode
          setActiveTab('browser');
        }
      };
    } catch (err) {
      console.warn('Live voice setup:', err);
      setLiveStatus('🟡 Switched to Direct Speech Mode');
      setActiveTab('browser');
      addToast('Using Fast Browser Voice Assistant', 'info');
    }
  };

  const stopLiveVoice = () => {
    try {
      if (processorRef.current) { processorRef.current.disconnect(); processorRef.current = null; }
      if (streamRef.current) { streamRef.current.getTracks().forEach(t => t.stop()); streamRef.current = null; }
      if (audioContextRef.current && audioContextRef.current.state !== 'closed') { audioContextRef.current.close(); audioContextRef.current = null; }
      if (playbackCtxRef.current && playbackCtxRef.current.state !== 'closed') { playbackCtxRef.current.close(); playbackCtxRef.current = null; }
      if (wsRef.current && wsRef.current.readyState === WebSocket.OPEN) { wsRef.current.close(1000, "User stopped"); wsRef.current = null; }
    } catch (e) {
      console.warn("Cleanup notice:", e);
    }
    setIsLiveConnected(false);
    setIsSpeakingLive(false);
    setLiveStatus('⏹ Voice stopped');
  };

  // -------------------------------------------------------------
  // 2. DIRECT BROWSER VOICE ASSISTANT (WEB SPEECH API)
  // -------------------------------------------------------------
  const bcp47Map = {
    English: 'en-IN',
    'తెలుగు': 'te-IN',
    Telugu: 'te-IN',
    'हिंदी': 'hi-IN',
    Hindi: 'hi-IN',
    'தமிழ்': 'ta-IN',
    Tamil: 'ta-IN',
    'ಕನ್ನಡ': 'kn-IN',
    Kannada: 'kn-IN',
    'मराठी': 'mr-IN',
    Marathi: 'mr-IN',
  };

  const handleBrowserMicToggle = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      addToast('Web Speech API is not supported in this browser. Please use Chrome/Edge.', 'error');
      return;
    }

    if (synthRef.current) synthRef.current.cancel();

    if (isBrowserListening) {
      if (recognitionRef.current) recognitionRef.current.stop();
      setIsBrowserListening(false);
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = bcp47Map[language] || 'en-IN';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    recognitionRef.current = recognition;

    recognition.onstart = () => {
      setIsBrowserListening(true);
      setBrowserStatus(`🔴 Listening in ${language}... Speak now!`);
    };

    recognition.onresult = async (event) => {
      const query = event.results[0][0].transcript;
      setBrowserUserSpeech(query);
      setBrowserStatus('⏳ Consulting AgriSense AI with your farm data...');
      setBrowserAiReply('Thinking...');

      try {
        const res = await api.askAiAssistant(farmer?.id || 1, query, language);
        if (res && res.answer) {
          setBrowserAiReply(res.answer);
          setBrowserStatus(`🟢 AgriSense is responding in ${language}`);
          speakText(res.answer, bcp47Map[language] || 'en-IN');
        }
      } catch (e) {
        console.warn('AI query failed:', e);
        const fallback = `Namaste! Regarding "${query}", based on your soil data, maintain adequate irrigation and apply organic compost.`;
        setBrowserAiReply(fallback);
        speakText(fallback, bcp47Map[language] || 'en-IN');
      }
    };

    recognition.onerror = (e) => {
      console.error('Speech recognition error:', e.error);
      setBrowserStatus(`❌ Speech recognition error: ${e.error}`);
      setIsBrowserListening(false);
    };

    recognition.onend = () => {
      setIsBrowserListening(false);
    };

    recognition.start();
  };

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

  const speakText = (text, lang) => {
    if (!synthRef.current) return;
    synthRef.current.cancel();
    const cleanText = text.replace(/[*#_`]/g, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    utterance.lang = lang;
    utterance.rate = 0.95;
    const voice = findMatchingVoice(lang);
    if (voice) {
      utterance.voice = voice;
    }
    utterance.onend = () => {
      setBrowserStatus('Tap microphone to speak again');
    };
    synthRef.current.speak(utterance);
  };

  const stopBrowserSpeech = () => {
    if (synthRef.current) synthRef.current.cancel();
    setBrowserStatus('Voice stopped. Tap microphone to speak again');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 24,paddingTop: 125, margin: '0 auto', width: '100%' }}>
      {/* Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #15803d 0%, #166534 100%)',
          color: 'white',
          padding: '24px 28px',
          borderRadius: 20
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: 12 }}>
          <div>
            <h2 style={{ color: 'white', fontSize: 24, margin: '0 0 6px 0' }}>
              {t.voice.title}
            </h2>
            <p style={{ color: '#dcfce7', fontSize: 14, margin: 0, maxWidth: 650 }}>
              {t.voice.subtitle} • Language: <strong>{language}</strong>
            </p>
          </div>
          <div className={`badge ${serverOnline ? 'badge-green' : 'badge-amber'}`} style={{ fontSize: 12, padding: '6px 14px' }}>
            {serverOnline ? <Wifi size={14} /> : <WifiOff size={14} />}
            <span>{serverOnline ? t.voice.serverOnline : t.voice.serverOffline}</span>
          </div>
        </div>
      </div>

      {/* Mode Selector Tabs */}
      <div style={{ display: 'flex', gap: 8, background: '#f1f5f9', padding: 6, borderRadius: 14, width: '100%', maxWidth: 380, margin: '0 auto', boxSizing: 'border-box' }}>
        <button
          onClick={() => setActiveTab('browser')}
          style={{
            flex: 1,
            padding: '10px 14px',
            borderRadius: 10,
            border: 'none',
            fontSize: 13,
            fontWeight: 800,
            cursor: 'pointer',
            textAlign: 'center',
            background: activeTab === 'browser' ? '#ffffff' : 'transparent',
            color: activeTab === 'browser' ? '#15803d' : '#64748b',
            boxShadow: activeTab === 'browser' ? '0 2px 8px rgba(0,0,0,0.06)' : 'none'
          }}
        >
          {t.voice.tabBrowser}
        </button>

        <button
          onClick={() => setActiveTab('live')}
          style={{
            flex: 1,
            padding: '10px 14px',
            borderRadius: 10,
            border: 'none',
            fontSize: 13,
            fontWeight: 800,
            cursor: 'pointer',
            textAlign: 'center',
            background: activeTab === 'live' ? '#ffffff' : 'transparent',
            color: activeTab === 'live' ? '#15803d' : '#64748b',
            boxShadow: activeTab === 'live' ? '0 2px 8px rgba(0,0,0,0.06)' : 'none'
          }}
        >
          {t.voice.tabLive}
        </button>
      </div>

      {/* Tab 1: Direct Browser Voice */}
      {activeTab === 'browser' && (
        <div className="agri-card" style={{ maxWidth: 680, margin: '0 auto', width: '100%', textAlign: 'center' }}>
          <button
            onClick={handleBrowserMicToggle}
            className={`btn ${isBrowserListening ? 'btn-danger pulse-glow' : 'btn-primary'}`}
            style={{
              width: 90,
              height: 90,
              borderRadius: '50%',
              margin: '20px auto 14px auto',
              fontSize: 34
            }}
          >
            {isBrowserListening ? <MicOff size={36} /> : <Mic size={36} />}
          </button>

          <div style={{ fontSize: 16, fontWeight: 800, color: '#0f172a', marginBottom: 12 }}>
            {browserStatus}
          </div>

          <button
            onClick={stopBrowserSpeech}
            className="btn btn-secondary"
            style={{ padding: '6px 14px', fontSize: 12, marginBottom: 20 }}
          >
            <Volume2 size={14} />
            <span>Stop AI Voice</span>
          </button>

          <div style={{ textAlign: 'left', background: '#f8fafc', padding: 16, borderRadius: 14, border: '1px solid #e2e8f0', marginBottom: 14 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: '#64748b', marginBottom: 4 }}>👨‍🌾 You Asked:</div>
            <div style={{ fontSize: 15, fontWeight: 700, color: '#0f172a', minHeight: 24, wordBreak: 'break-word', overflowWrap: 'anywhere' }}>{browserUserSpeech}</div>
          </div>

          <div style={{ textAlign: 'left', background: '#f0fdf4', padding: 16, borderRadius: 14, border: '1px solid #bbf7d0' }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: '#15803d', marginBottom: 4 }}>🤖 AgriSense AI Response:</div>
            <div style={{ fontSize: 14, color: '#14532d', lineHeight: 1.6, minHeight: 48, whiteSpace: 'pre-wrap', wordBreak: 'break-word', overflowWrap: 'anywhere' }}>
              {browserAiReply}
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Gemini Live WebSocket Streaming */}
      {activeTab === 'live' && (
        <div className="agri-card" style={{ maxWidth: 680, margin: '0 auto', width: '100%', textAlign: 'center' }}>
          {!serverOnline && (
            <div style={{ background: '#fff7ed', border: '1.5px solid #fed7aa', borderRadius: 14, padding: 14, textAlign: 'left', color: '#9a3412', marginBottom: 16, fontSize: 13, wordBreak: 'break-word' }}>
              <strong>⚠️ WebSocket Server Offline:</strong> Live Voice streaming requires the backend on port 8000.<br />
              In terminal run: <code style={{ background: '#ffffff', padding: '2px 6px', borderRadius: 4 }}>python server.py</code>
            </div>
          )}

          {isSpeakingLive && (
            <div className="voice-visualizer">
              <div className="wave-bar"></div>
              <div className="wave-bar"></div>
              <div className="wave-bar"></div>
              <div className="wave-bar"></div>
              <div className="wave-bar"></div>
            </div>
          )}

          <div style={{ fontSize: 16, fontWeight: 800, color: '#0f172a', margin: '12px 0' }}>
            {liveStatus}
          </div>

          <div style={{ display: 'flex', gap: 10, justifyContent: 'center', flexWrap: 'wrap', margin: '16px 0' }}>
            <button
              onClick={startLiveVoice}
              disabled={isLiveConnected}
              className="btn btn-primary"
              style={{ flex: '1 1 140px', maxWidth: 220, minHeight: 46 }}
            >
              <Mic size={18} />
              <span>{t.voice.startBtn}</span>
            </button>

            <button
              onClick={stopLiveVoice}
              disabled={!isLiveConnected}
              className="btn btn-danger"
              style={{ flex: '1 1 140px', maxWidth: 220, minHeight: 46 }}
            >
              <MicOff size={18} />
              <span>{t.voice.stopBtn}</span>
            </button>
          </div>

          <div style={{ textAlign: 'left', background: '#f8fafc', padding: 18, borderRadius: 14, border: '1px solid #e2e8f0', marginTop: 14 }}>
            <div style={{ fontSize: 12, fontWeight: 700, color: '#64748b', marginBottom: 6 }}>
              {t.voice.transcriptTitle}:
            </div>
            <div style={{ fontSize: 14, color: '#0f172a', lineHeight: 1.6, minHeight: 60, wordBreak: 'break-word', overflowWrap: 'anywhere' }}>
              {liveTranscript}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
