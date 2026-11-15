import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  FileDown,
  AlertCircle,
  Heart,
  ShieldCheck,
  Activity,
  ChevronDown,
  RefreshCw
} from 'lucide-react';
import { api } from '../services/api';
import RiskGauge from '../components/RiskGauge';
import ShapExplainer from '../components/ShapExplainer';

export default function PredictiveDiagnostics({ initialPatient }) {
  const [patients, setPatients] = useState([]);
  const [selectedPatient, setSelectedPatient] = useState(initialPatient || null);
  const [diagnosticResult, setDiagnosticResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeDiseaseTab, setActiveDiseaseTab] = useState('heart_disease');

  useEffect(() => {
    loadPatients();
  }, []);

  useEffect(() => {
    if (initialPatient) {
      setSelectedPatient(initialPatient);
      runDiagnosisForPatient(initialPatient);
    }
  }, [initialPatient]);

  const loadPatients = async () => {
    try {
      const data = await api.getPatients();
      setPatients(data);
      if (!selectedPatient && data.length > 0) {
        setSelectedPatient(data[0]);
        runDiagnosisForPatient(data[0]);
      }
    } catch (err) {
      console.error('Failed to load patients for diagnosis:', err);
    }
  };

  const runDiagnosisForPatient = async (patient) => {
    if (!patient) return;
    setLoading(true);
    try {
      const v = patient.latest_vitals || {};
      const payload = {
        patient_id: patient.id,
        age: patient.age,
        gender: patient.gender,
        systolic_bp: v.systolic_bp || 135,
        diastolic_bp: v.diastolic_bp || 85,
        heart_rate: v.heart_rate || 72,
        fasting_glucose: v.fasting_glucose || 110,
        total_cholesterol: v.total_cholesterol || 210,
        bmi: v.bmi || 27.0,
        smoking_status: v.smoking_status || false,
        physical_activity_hours: v.physical_activity_hours || 2.5,
      };

      const result = await api.predictDiseaseRisk(payload);
      setDiagnosticResult(result);
    } catch (err) {
      console.error('Diagnosis prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePatientChange = (e) => {
    const patientId = Number(e.target.value);
    const p = patients.find((item) => item.id === patientId);
    if (p) {
      setSelectedPatient(p);
      runDiagnosisForPatient(p);
    }
  };

  const handleDownloadPdf = () => {
    if (!selectedPatient) return;
    const url = api.getPdfReportUrl(selectedPatient.id);
    window.open(url, '_blank');
  };

  const activeRiskData = diagnosticResult?.risks?.[activeDiseaseTab] || (diagnosticResult?.risks && Object.values(diagnosticResult.risks)[0]);

  return (
    <div className="space-y-6">
      {/* Top Patient Control Bar */}
      <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center space-x-3 w-full sm:w-auto">
          <div className="p-2.5 rounded-xl bg-blue-50 text-blue-600">
            <Activity className="w-5 h-5" />
          </div>
          <div>
            <label className="block text-[10px] font-bold text-slate-400 uppercase tracking-wider">
              Evaluating Patient
            </label>
            <div className="relative mt-0.5">
              <select
                value={selectedPatient?.id || ''}
                onChange={handlePatientChange}
                className="font-bold text-slate-800 text-sm bg-transparent pr-7 py-0.5 focus:outline-hidden cursor-pointer"
              >
                {patients.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.full_name} ({p.patient_code}) — {p.age}y {p.gender}
                  </option>
                ))}
              </select>
            </div>
          </div>
        </div>

        <div className="flex items-center space-x-2.5 w-full sm:w-auto justify-end">
          <button
            onClick={() => runDiagnosisForPatient(selectedPatient)}
            disabled={loading}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs transition-colors"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
            <span>Re-evaluate AI</span>
          </button>
          <button
            onClick={handleDownloadPdf}
            className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md shadow-blue-600/20 transition-all"
          >
            <FileDown className="w-4 h-4" />
            <span>Export Verified PDF</span>
          </button>
        </div>
      </div>

      {/* Overall Health Score Card */}
      {diagnosticResult && (
        <div className="bg-gradient-to-r from-blue-900 via-indigo-950 to-slate-900 rounded-3xl p-6 text-white shadow-xl flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="space-y-1 text-center md:text-left">
            <div className="inline-flex items-center space-x-1.5 text-xs text-cyan-300 font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Multi-Condition Composite Risk Prognosis (4 Conditions)</span>
            </div>
            <h2 className="text-xl font-bold tracking-tight">
              Patient Cardiometabolic & Renal Health Index
            </h2>
            <p className="text-xs text-slate-300 max-w-lg">
              Integrated prognostic score synthesizing hemodynamics, glycemic trajectories, lipid panels, and renal indicators.
            </p>
          </div>

          <div className="flex items-center space-x-4 bg-white/10 backdrop-blur-md px-6 py-4 rounded-2xl border border-white/10">
            <div className="text-center">
              <span className="block text-3xl font-black text-cyan-300">
                {diagnosticResult.overall_health_score}
              </span>
              <span className="text-[10px] text-slate-300 uppercase font-semibold">
                Score / 100
              </span>
            </div>
            <div className="h-10 w-px bg-white/20"></div>
            <div className="text-xs">
              <span className="block font-bold text-white">
                {diagnosticResult.overall_health_score >= 70 ? 'Favorable Prognosis' : 'Clinical Attention Advised'}
              </span>
              <span className="text-slate-300 text-[11px]">
                {diagnosticResult.overall_health_score >= 70 ? 'Low acute chronic vulnerability' : 'Targeted lifestyle intervention warranted'}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* 4 Animated Risk Gauges Grid */}
      {diagnosticResult && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {Object.entries(diagnosticResult.risks).map(([key, data]) => {
            const isSelected = activeDiseaseTab === key;
            return (
              <div
                key={key}
                onClick={() => setActiveDiseaseTab(key)}
                className={`cursor-pointer transition-transform ${isSelected ? 'scale-[1.02]' : 'hover:scale-[1.01]'}`}
              >
                <RiskGauge
                  percentage={data.risk_percentage}
                  level={data.risk_level}
                  diseaseName={data.disease_type}
                  subtitle={isSelected ? '● Inspected for XAI' : 'Click to inspect biomarker drivers'}
                />
              </div>
            );
          })}
        </div>
      )}

      {/* Explainable AI + Clinical Recommendations Row */}
      {activeRiskData && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* XAI Diverging Bar Chart (7 cols) */}
          <div className="lg:col-span-7">
            <ShapExplainer
              featureContributions={activeRiskData.feature_contributions}
              diseaseTitle={activeRiskData.disease_type}
            />
          </div>

          {/* Clinical Directives & Recommendations (5 cols) */}
          <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs flex flex-col justify-between">
            <div>
              <div className="flex items-center space-x-2 mb-4">
                <ShieldCheck className="w-5 h-5 text-blue-600" />
                <h3 className="font-bold text-slate-800 text-sm">
                  Clinical Action Directives: {activeRiskData.disease_type}
                </h3>
              </div>
              <p className="text-xs text-slate-500 mb-4">
                Evidence-based preventative interventions tailored to {selectedPatient?.full_name}'s specific biomarker profile:
              </p>

              <div className="space-y-3">
                {activeRiskData.clinical_recommendations.map((rec, i) => (
                  <div
                    key={i}
                    className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-start space-x-3 text-xs text-slate-700"
                  >
                    <span className="w-5 h-5 rounded-full bg-blue-100 text-blue-700 font-bold flex items-center justify-center shrink-0 text-[10px] mt-0.5">
                      {i + 1}
                    </span>
                    <span className="leading-relaxed">{rec}</span>
                  </div>
                ))}
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-100 text-[11px] text-slate-400">
              Correlated with clinical guidelines: ACC/AHA Prevention Guidelines, ADA Standards of Care, & KDIGO Guidelines.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
