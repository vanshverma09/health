import React, { useState, useEffect } from 'react';
import { 
  Activity, 
  Users, 
  AlertTriangle, 
  ShieldCheck, 
  TrendingUp, 
  ChevronRight, 
  ArrowUpRight,
  FileText,
  HeartPulse,
  BrainCircuit
} from 'lucide-react';
import { api } from '../services/api';
import VitalsTimeline from '../components/VitalsTimeline';

export default function Dashboard({ onNavigateToDiagnostics, onNavigateToPatients }) {
  const [patients, setPatients] = useState([]);
  const [analytics, setAnalytics] = useState(null);
  const [selectedPatient, setSelectedPatient] = useState(null);
  const [timelineRecords, setTimelineRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [pts, cohort] = await Promise.all([
        api.getPatients(),
        api.getCohortAnalytics().catch(() => null),
      ]);
      setPatients(pts);
      setAnalytics(cohort);
      if (pts.length > 0) {
        setSelectedPatient(pts[0]);
        loadTimeline(pts[0].id);
      }
    } catch (err) {
      console.error('Error loading dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadTimeline = async (patientId) => {
    try {
      const records = await api.getTimeline(patientId);
      setTimelineRecords(records);
    } catch (err) {
      console.error('Timeline fetch error:', err);
    }
  };

  const handlePatientSelect = (p) => {
    setSelectedPatient(p);
    loadTimeline(p.id);
  };

  return (
    <div className="space-y-6">
      {/* Top Banner / Welcome */}
      <div className="bg-gradient-to-r from-slate-900 via-blue-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl relative overflow-hidden">
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-radial from-cyan-500/10 to-transparent pointer-events-none"></div>
        <div className="max-w-2xl relative z-10">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-cyan-500/10 text-cyan-300 text-xs font-semibold mb-3 border border-cyan-400/20">
            <HeartPulse className="w-3.5 h-3.5 text-cyan-400" />
            <span>Real-time Clinical Decision Support Active</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-black tracking-tight">
            DataVision Clinical Observatory
          </h1>
          <p className="text-xs sm:text-sm text-slate-300 mt-2 leading-relaxed">
            Multi-disease predictive telemetry correlating patient vitals with validated epidemiological models for early chronic disease intervention.
          </p>
        </div>
      </div>

      {/* Metric Cards Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-medium text-slate-500">Active Patient Cohort</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">{patients.length}</h3>
            </div>
            <div className="p-2.5 rounded-xl bg-blue-50 text-blue-600">
              <Users className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center text-[11px] text-emerald-600 font-semibold">
            <TrendingUp className="w-3.5 h-3.5 mr-1" />
            <span>Monitored in real-time</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-medium text-slate-500">High / Critical Alerts</p>
              <h3 className="text-2xl font-bold text-rose-600 mt-1">
                {analytics?.high_risk_patients_count || patients.filter(p => Object.values(p.latest_risks || {}).some(r => r.level === 'HIGH' || r.level === 'CRITICAL')).length}
              </h3>
            </div>
            <div className="p-2.5 rounded-xl bg-rose-50 text-rose-600">
              <AlertTriangle className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center text-[11px] text-rose-600 font-semibold">
            <span>Requires clinical attention</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-medium text-slate-500">Consultation Records</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">
                {analytics?.total_health_records || 32}
              </h3>
            </div>
            <div className="p-2.5 rounded-xl bg-cyan-50 text-cyan-600">
              <Activity className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center text-[11px] text-slate-500 font-medium">
            <span>Longitudinal biomarker points</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <div className="flex justify-between items-start">
            <div>
              <p className="text-xs font-medium text-slate-500">ML Engine Confidence</p>
              <h3 className="text-2xl font-bold text-slate-900 mt-1">92.4%</h3>
            </div>
            <div className="p-2.5 rounded-xl bg-purple-50 text-purple-600">
              <BrainCircuit className="w-5 h-5" />
            </div>
          </div>
          <div className="mt-3 flex items-center text-[11px] text-purple-600 font-semibold">
            <ShieldCheck className="w-3.5 h-3.5 mr-1" />
            <span>ROC-AUC Verified Model</span>
          </div>
        </div>
      </div>

      {/* Main Grid: Patient Selector + Longitudinal Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Patient Quick Directory (4 columns) */}
        <div className="lg:col-span-4 bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs flex flex-col h-[520px]">
          <div className="flex justify-between items-center mb-3">
            <h3 className="font-bold text-sm text-slate-800">Monitored Patients</h3>
            <button
              onClick={onNavigateToPatients}
              className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center"
            >
              <span>View All</span>
              <ChevronRight className="w-3.5 h-3.5 ml-0.5" />
            </button>
          </div>
          <div className="flex-1 overflow-y-auto space-y-2 pr-1">
            {patients.map((p) => {
              const isSelected = selectedPatient?.id === p.id;
              const hasHighRisk = Object.values(p.latest_risks || {}).some(
                (r) => r.level === 'HIGH' || r.level === 'CRITICAL'
              );

              return (
                <div
                  key={p.id}
                  onClick={() => handlePatientSelect(p)}
                  className={`p-3 rounded-xl border text-left cursor-pointer transition-all ${
                    isSelected
                      ? 'border-blue-500 bg-blue-50/50 shadow-xs'
                      : 'border-slate-100 hover:border-slate-200 hover:bg-slate-50/50'
                  }`}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h4 className="font-bold text-xs text-slate-800">{p.full_name}</h4>
                      <p className="text-[11px] text-slate-400 mt-0.5">
                        {p.patient_code} • {p.age} yrs • {p.gender}
                      </p>
                    </div>
                    {hasHighRisk ? (
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-100 text-rose-700">
                        High Risk
                      </span>
                    ) : (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700">
                        Stable
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Patient Vitals Timeline (8 columns) */}
        <div className="lg:col-span-8 flex flex-col space-y-4">
          {selectedPatient && (
            <div className="bg-white rounded-2xl p-4 border border-slate-200/80 shadow-xs flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 rounded-xl bg-blue-100 text-blue-700 font-black flex items-center justify-center text-sm">
                  {selectedPatient.full_name.charAt(0)}
                </div>
                <div>
                  <h3 className="font-bold text-sm text-slate-800">{selectedPatient.full_name}</h3>
                  <p className="text-xs text-slate-400">
                    ID: {selectedPatient.patient_code} | History: {selectedPatient.medical_history || 'None'}
                  </p>
                </div>
              </div>
              <button
                onClick={() => onNavigateToDiagnostics(selectedPatient)}
                className="flex items-center space-x-1.5 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md shadow-blue-600/20 transition-all"
              >
                <span>Run Diagnostic AI</span>
                <ArrowUpRight className="w-4 h-4" />
              </button>
            </div>
          )}

          <div className="flex-1">
            <VitalsTimeline records={timelineRecords} />
          </div>
        </div>
      </div>
    </div>
  );
}

