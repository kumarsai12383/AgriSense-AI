import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import LoginModal from './components/LoginModal';
import Dashboard from './components/Dashboard';
import CropRecommendation from './components/CropRecommendation';
import SoilHealth from './components/SoilHealth';
import IrrigationAdvisor from './components/IrrigationAdvisor';
import FertilizerAdvisor from './components/FertilizerAdvisor';
import DiseaseDetection from './components/DiseaseDetection';
import MandiPrices from './components/MandiPrices';
import GovtSchemes from './components/GovtSchemes';
import VoiceAssistant from './components/VoiceAssistant';
import AiChat from './components/AiChat';
import HelpCenter from './components/HelpCenter';
import FarmData from './components/FarmData';
import { api } from './api';

export default function App() {
  const [farmer, setFarmer] = useState(() => {
    const saved = localStorage.getItem('agrisense_farmer');
    return saved ? JSON.parse(saved) : null;
  });

  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('agrisense_language') || 'English';
  });

  const [currentTab, setCurrentTab] = useState('dashboard');
  const [farmData, setFarmData] = useState(null);
  const [latestCrop, setLatestCrop] = useState(null);
  const [sensorOnline, setSensorOnline] = useState(false);
  const [serverOnline, setServerOnline] = useState(false);
  const [toasts, setToasts] = useState([]);

  const addToast = (message, type = 'info') => {
    const id = Date.now();
    setToasts((prev) => [...prev, { id, message, type }]);
    setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
    }, 4000);
  };

  // Sync language with localStorage
  const handleLanguageChange = (newLang) => {
    setLanguage(newLang);
    localStorage.setItem('agrisense_language', newLang);
  };

  // Login handler
  const handleLoginSuccess = (farmerData) => {
    setFarmer(farmerData);
    localStorage.setItem('agrisense_farmer', JSON.stringify(farmerData));
    if (farmerData.language) {
      setLanguage(farmerData.language);
      localStorage.setItem('agrisense_language', farmerData.language);
    }
  };

  // Logout handler
  const handleLogout = () => {
    setFarmer(null);
    localStorage.removeItem('agrisense_farmer');
    addToast('Logged out of farmer profile', 'info');
  };

  // Fetch initial farm data and sensor status
  const loadFarmData = async () => {
    if (!farmer?.id) return;
    try {
      const [dataRes, cropRes, sensorRes, healthRes] = await Promise.allSettled([
        api.getLatestFarmData(farmer.id),
        api.getLatestCrop(farmer.id),
        api.getSensorStatus(farmer.id),
        api.checkHealth()
      ]);

      if (dataRes.status === 'fulfilled' && dataRes.value?.data) {
        setFarmData(dataRes.value.data);
      }
      if (cropRes.status === 'fulfilled' && cropRes.value?.data) {
        setLatestCrop(cropRes.value.data);
      }
      if (sensorRes.status === 'fulfilled' && sensorRes.value) {
        setSensorOnline(sensorRes.value.connected === true);
      }
      if (healthRes.status === 'fulfilled') {
        setServerOnline(healthRes.value?.status === 'healthy');
      }
    } catch (e) {
      console.warn('Initial data load warning:', e);
    }
  };

  useEffect(() => {
    loadFarmData();
    const interval = setInterval(loadFarmData, 10000);
    return () => clearInterval(interval);
  }, [farmer?.id]);

  return (
    <div className="app-container" style={{ flexDirection: 'column' }}>
      {/* Toast Notifications */}
      <div className="toast-container">
        {toasts.map((t) => (
          <div key={t.id} className="toast">
            <span>{t.type === 'success' ? '✅' : t.type === 'error' ? '⚠️' : 'ℹ️'}</span>
            <span>{t.message}</span>
          </div>
        ))}
      </div>

      {/* Login Modal if not logged in */}
      {!farmer && (
        <LoginModal
          language={language}
          setLanguage={handleLanguageChange}
          onLoginSuccess={handleLoginSuccess}
          addToast={addToast}
        />
      )}

      {/* Main Navbar */}
      <Navbar
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        language={language}
        setLanguage={handleLanguageChange}
        farmer={farmer}
        onLogout={handleLogout}
        sensorOnline={sensorOnline}
        serverOnline={serverOnline}
      />

      {/* Main Content Area */}
      <main className="main-content">
        {currentTab === 'dashboard' && (
          <Dashboard
            farmer={farmer}
            language={language}
            farmData={farmData}
            latestCrop={latestCrop}
            setCurrentTab={setCurrentTab}
            sensorStatus={sensorOnline}
            onAutofillAndPredict={() => setCurrentTab('crop')}
            onDataUpdated={(updated) => {
              setFarmData((prev) => ({ ...prev, ...updated }));
              loadFarmData();
            }}
            addToast={addToast}
          />
        )}

        {currentTab === 'crop' && (
          <CropRecommendation
            farmer={farmer}
            language={language}
            farmData={farmData}
            latestCrop={latestCrop}
            setCurrentTab={setCurrentTab}
            onPredictionSaved={(newPred) => {
              setLatestCrop(newPred);
              loadFarmData();
            }}
            addToast={addToast}
          />
        )}

        {currentTab === 'soil' && (
          <SoilHealth
            farmer={farmer}
            language={language}
            farmData={farmData}
            onNavigate={(tab) => setCurrentTab(tab)}
          />
        )}

        {currentTab === 'irrigation' && (
          <IrrigationAdvisor
            farmer={farmer}
            language={language}
            farmData={farmData}
            latestCrop={latestCrop}
            addToast={addToast}
          />
        )}

        {currentTab === 'fertilizer' && (
          <FertilizerAdvisor
            farmer={farmer}
            language={language}
            farmData={farmData}
            latestCrop={latestCrop}
          />
        )}

        {currentTab === 'disease' && (
          <DiseaseDetection
            farmer={farmer}
            language={language}
            addToast={addToast}
          />
        )}

        {currentTab === 'mandi' && (
          <MandiPrices
            farmer={farmer}
            language={language}
            setCurrentTab={setCurrentTab}
          />
        )}

        {currentTab === 'schemes' && (
          <GovtSchemes
            farmer={farmer}
            language={language}
          />
        )}

        {currentTab === 'voice' && (
          <VoiceAssistant
            farmer={farmer}
            language={language}
            serverOnline={serverOnline}
            addToast={addToast}
          />
        )}

        {currentTab === 'chat' && (
          <AiChat
            farmer={farmer}
            language={language}
            farmData={farmData}
            latestCrop={latestCrop}
          />
        )}

        {currentTab === 'help' && (
          <HelpCenter
            language={language}
            setCurrentTab={setCurrentTab}
          />
        )}

        {currentTab === 'sensors' && (
          <FarmData
            farmer={farmer}
            language={language}
            farmData={farmData}
            onDataUpdated={() => {
              loadFarmData();
              addToast('Farm telemetry refreshed successfully', 'success');
            }}
            addToast={addToast}
          />
        )}
      </main>
    </div>
  );
}
