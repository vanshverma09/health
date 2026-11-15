import React, { useState, useEffect } from 'react';
import { 
  Users, 
  Search, 
  Filter, 
  UserPlus, 
  Activity, 
  FileDown, 
  Sparkles,
  Heart,
  Droplet
} from 'lucide-react';
import { api } from '../services/api';
import NewPatientModal from '../components/NewPatientModal';
import NewRecordModal from '../components/NewRecordModal';

export default function Patients({ onSelectPatientForDiagnostics }) {
  const [patients, setPatients] = useState([]);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [loading, setLoading] = useState(true);

  // Modals state
  const [isAddPatientOpen, setIsAddPatientOpen] = useState(false);
  const [selectedPatientForRecord, setSelectedPatientForRecord] = useState(null);

  useEffect(() => {
    fetchPatients();
  }, [search, riskFilter]);

  const fetchPatients = async () => {
    try {
      setLoading(true);
      const data = await api.getPatients(search, riskFilter);
      setPatients(data);
    } catch (err) {
      console.error('Failed to load patients:', err);
    } finally {
      setLoading(false);
    }
  };

  const handlePatientCreated = (newPatient) => {
    fetchPatients();
  };

  const handleRecordCreated = () => {
    fetchPatients();
  };

  const handleDownloadPdf = (patientId) => {
    const url = api.getPdfReportUrl(patientId);
    window.open(url, '_blank');
  };

  return (
    <div className="space-y-6">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold text-slate-800 tracking-tight">Patient Directory</h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Manage patient health records, longitudinal vitals, and diagnostic histories
          </p>
        </div>
        <button
          onClick={() => setIsAddPatientOpen(true)}
          className="flex items-center space-x-2 px-4 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs shadow-md shadow-blue-600/20 transition-all self-start sm:self-auto"
        >
          <UserPlus className="w-4 h-4" />
          <span>Register New Patient</span>
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white rounded-2xl p-4 border border-slate-200/80 shadow-xs flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by patient name or ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs border border-slate-200 rounded-xl focus:ring-2 focus:ring-blue-500 focus:outline-hidden"
          />
        </div>

        {/* Filter Pills */}
        <div className="flex items-center space-x-2 w-full sm:w-auto overflow-x-auto pb-1 sm:pb-0">
          <Filter className="w-3.5 h-3.5 text-slate-400 shrink-0 ml-1" />
          <span className="text-xs text-slate-400 font-medium shrink-0">Filter Risk:</span>
          {['ALL', 'CRITICAL', 'HIGH', 'MODERATE', 'LOW'].map((filter) => (
            <button
              key={filter}
              onClick={() => setRiskFilter(filter)}
              className={`px-3 py-1 rounded-lg text-xs font-semibold whitespace-nowrap transition-all ${
                riskFilter === filter
                  ? 'bg-slate-900 text-white shadow-xs'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {filter}
            </button>
          ))}
        </div>
      </div>

      {/* Patient Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {patients.map((p) => {
          const v = p.latest_vitals;
          const risks = p.latest_risks || {};

          return (
            <div
              key={p.id}
              className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow flex flex-col justify-between"
            >
              <div>
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-10 h-10 rounded-xl bg-slate-100 text-slate-700 font-black flex items-center justify-center text-sm border border-slate-200">
                      {p.full_name.charAt(0)}
                    </div>
                    <div>
                      <h3 className="font-bold text-sm text-slate-800">{p.full_name}</h3>
                      <p className="text-[11px] text-slate-400 font-mono">
                        {p.patient_code} • {p.age}y • {p.gender} • {p.blood_group || 'O+'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* Latest Vitals Snapshot */}
                <div className="mt-4 p-3 rounded-xl bg-slate-50 border border-slate-100">
                  <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-1.5">
                    Latest Vitals Snapshot
                  </div>
                  {v ? (
                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div className="bg-white p-1.5 rounded-lg border border-slate-100">
                        <span className="block text-[10px] text-slate-400">BP (mmHg)</span>
                        <span className="font-bold text-xs text-slate-800">
                          {v.systolic_bp}/{v.diastolic_bp}
                        </span>
                      </div>
                      <div className="bg-white p-1.5 rounded-lg border border-slate-100">
                        <span className="block text-[10px] text-slate-400">Glucose</span>
                        <span className="font-bold text-xs text-slate-800">{v.fasting_glucose}</span>
                      </div>
                      <div className="bg-white p-1.5 rounded-lg border border-slate-100">
                        <span className="block text-[10px] text-slate-400">BMI</span>
                        <span className="font-bold text-xs text-slate-800">{v.bmi}</span>
                      </div>
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 text-center py-1">No vitals on file</p>
                  )}
                </div>

                {/* Risk Badges */}
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {Object.entries(risks).map(([disease, info]) => {
                    const isHigh = info.level === 'HIGH' || info.level === 'CRITICAL';
                    return (
                      <span
                        key={disease}
                        className={`text-[10px] font-bold px-2 py-0.5 rounded-md ${
                          isHigh ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'
                        }`}
                      >
                        {disease.replace('_', ' ')}: {info.level}
                      </span>
                    );
                  })}
                </div>
              </div>

              {/* Action Buttons */}
              <div className="mt-5 pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                <button
                  onClick={() => setSelectedPatientForRecord(p)}
                  className="flex-1 flex items-center justify-center space-x-1 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 text-xs font-semibold transition-colors"
                >
                  <Activity className="w-3.5 h-3.5" />
                  <span>Checkup</span>
                </button>
                <button
                  onClick={() => onSelectPatientForDiagnostics(p)}
                  className="flex-1 flex items-center justify-center space-x-1 py-2 rounded-xl bg-blue-600 hover:bg-blue-700 text-white text-xs font-bold shadow-xs transition-colors"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>Diagnosis</span>
                </button>
                <button
                  onClick={() => handleDownloadPdf(p.id)}
                  title="Export Clinical PDF Report"
                  className="p-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-600 transition-colors"
                >
                  <FileDown className="w-4 h-4" />
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {/* Modals */}
      <NewPatientModal
        isOpen={isAddPatientOpen}
        onClose={() => setIsAddPatientOpen(false)}
        onPatientCreated={handlePatientCreated}
      />
      <NewRecordModal
        isOpen={!!selectedPatientForRecord}
        patient={selectedPatientForRecord}
        onClose={() => setSelectedPatientForRecord(null)}
        onRecordCreated={handleRecordCreated}
      />
    </div>
  );
}

