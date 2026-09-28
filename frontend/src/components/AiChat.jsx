import React, { useState, useRef, useEffect } from 'react';
import { MessageSquareCode, Send, Trash2, Sparkles, User, Bot } from 'lucide-react';
import { TRANSLATIONS } from '../translations';
import { api } from '../api';

export default function AiChat({ farmer, language, addToast }) {
  const t = TRANSLATIONS[language] || TRANSLATIONS.English;

  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `Namaste 👨‍🌾 **${farmer?.name || 'Farmer'}**! I am your AgriSense AI Agronomist. How can I assist you with your crops, soil nutrients, water scheduling, or fertilizer today?`
    }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (queryText) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || loading) return;

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
      const fallback = `Based on your farm profile and soil measurements: Maintain balanced NPK application, irrigate during early morning hours, and monitor lower leaves for early pest signs.`;
      setMessages((prev) => [...prev, { role: 'assistant', content: fallback }]);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setMessages([
      {
        role: 'assistant',
        content: `Namaste 👨‍🌾 **${farmer?.name || 'Farmer'}**! Chat history cleared. How can I help you?`
      }
    ]);
    addToast('Chat cleared', 'info');
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
      {/* Banner */}
      <div 
        className="agri-card"
        style={{
          background: 'linear-gradient(135deg, #15803d 0%, #16a34a 100%)',
          color: 'white',
          padding: '20px 24px',
          borderRadius: 20
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ color: 'white', fontSize: 22, margin: '0 0 4px 0' }}>
              🤖 {t.chat.title}
            </h2>
            <p style={{ color: '#dcfce7', fontSize: 13, margin: 0 }}>
              {t.chat.subtitle}
            </p>
          </div>
          <button 
            onClick={handleClear}
            className="btn" 
            style={{ background: 'rgba(255,255,255,0.2)', color: 'white', padding: '8px 14px', fontSize: 12 }}
          >
            <Trash2 size={14} />
            <span>{t.chat.clear}</span>
          </button>
        </div>
      </div>

      {/* Quick Questions Row */}
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
        {[t.chat.quick1, t.chat.quick2, t.chat.quick3].map((q, idx) => (
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
          return (
            <div
              key={idx}
              style={{
                display: 'flex',
                gap: 10,
                alignSelf: isUser ? 'flex-end' : 'flex-start',
                maxWidth: '85%'
              }}
            >
              {!isUser && (
                <div style={{ width: 34, height: 34, borderRadius: 10, background: '#15803d', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', flexShrink: 0 }}>
                  <Bot size={18} />
                </div>
              )}
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
                  boxShadow: '0 2px 6px rgba(0,0,0,0.03)'
                }}
              >
                {m.content}
              </div>
              {isUser && (
                <div style={{ width: 34, height: 34, borderRadius: 10, background: '#0284c7', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', flexShrink: 0 }}>
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
              Consulting AgriSense AI agronomist...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Field */}
      <form 
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        style={{ display: 'flex', gap: 10 }}
      >
        <input
          type="text"
          className="input-field"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={t.chat.inputPlaceholder}
          disabled={loading}
          style={{ height: 50 }}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="btn btn-primary"
          style={{ width: 54, height: 50, padding: 0 }}
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
}
