import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Patients from './pages/Patients';
import PredictiveDiagnostics from './pages/PredictiveDiagnostics';
import WhatIfSimulator from './components/WhatIfSimulator';
import PopulationAnalytics from './pages/PopulationAnalytics';
import Login from './pages/Login';
import { api, getAuthToken, setAuthToken } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentUser, setCurrentUser] = useState(null);
  const [selectedPatientForDiagnostics, setSelectedPatientForDiagnostics] = useState(null);
  const [isInitializing, setIsInitializing] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = getAuthToken();
    if (token) {
      try {
        const user = await api.getMe();
        setCurrentUser(user);
      } catch (err) {
        console.warn('Session expired or invalid token:', err);
        setAuthToken(null);
        setCurrentUser(null);
      }
    }
    setIsInitializing(false);
  };

  const handleLoginSuccess = (user) => {
    setCurrentUser(user);
    setActiveTab('dashboard');
  };

  const handleLogout = () => {
    setAuthToken(null);
    setCurrentUser(null);
  };

  const handleNavigateToDiagnostics = (patient) => {
    setSelectedPatientForDiagnostics(patient);
    setActiveTab('diagnostics');
  };

  const handleNavigateToPatients = () => {
    setActiveTab('patients');
  };

  if (isInitializing) {
    return (
      <div className="min-h-screen bg-slate-950 flex items-center justify-center text-white">
        <div className="flex flex-col items-center space-y-3">
          <div className="w-8 h-8 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs font-semibold text-slate-400">Initializing DataVision Health Observatory...</p>
        </div>
      </div>
    );
  }

  if (!currentUser) {
    return <Login onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar Navigation */}
      <Sidebar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentDoctor={currentUser}
        onLogout={handleLogout}
      />

      {/* Main Clinical Viewport */}
      <main className="flex-1 ml-64 p-6 sm:p-8 max-w-7xl mx-auto min-h-screen">
        {activeTab === 'dashboard' && (
          <Dashboard
            onNavigateToDiagnostics={handleNavigateToDiagnostics}
            onNavigateToPatients={handleNavigateToPatients}
          />
        )}

        {activeTab === 'patients' && (
          <Patients
            onSelectPatientForDiagnostics={handleNavigateToDiagnostics}
          />
        )}

        {activeTab === 'diagnostics' && (
          <PredictiveDiagnostics
            initialPatient={selectedPatientForDiagnostics}
          />
        )}

        {activeTab === 'what-if' && (
          <WhatIfSimulator
            patient={selectedPatientForDiagnostics}
          />
        )}

        {activeTab === 'population' && (
          <PopulationAnalytics />
        )}
      </main>
    </div>
  );
}
