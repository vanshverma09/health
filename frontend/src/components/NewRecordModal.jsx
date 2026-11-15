import React, { useState } from 'react';
import { X, Activity, Save } from 'lucide-react';
import { api } from '../services/api';

export default function NewRecordModal({ isOpen, onClose, patient, onRecordCreated }) {
  const [formData, setFormData] = useState({
    patient_id: patient?.id,
    systolic_bp: 125,
    diastolic_bp: 82,
    heart_rate: 72,
    fasting_glucose: 98,
    total_cholesterol: 195,
    bmi: 25.2,
    smoking_status: false,
    alcohol_consumption: false,
    physical_activity_hours: 3.0,
    notes: 'Routine clinical consultation checkup.',
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  if (!isOpen || !patient) return null;

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const payload = { ...formData, patient_id: patient.id };
      const record = await api.addHealthRecord(payload);
      
      // Also automatically trigger diagnostic prediction with these new vitals
      await api.predictDiseaseRisk({
        patient_id: patient.id,
        age: patient.age,
        gender: patient.gender,
        systolic_bp: payload.systolic_bp,
        diastolic_bp: payload.diastolic_bp,
        heart_rate: payload.heart_rate,
        fasting_glucose: payload.fasting_glucose,
        total_cholesterol: payload.total_cholesterol,
        bmi: payload.bmi,
        smoking_status: payload.smoking_status,
        physical_activity_hours: payload.physical_activity_hours,
      });

      onRecordCreated(record);
      onClose();
    } catch (err) {
      setError(err.message || 'Failed to record vitals');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4">
      <div className="bg-white rounded-2xl max-w-lg w-full border border-slate-200 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200">
        {/* Header */}
        <div className="px-6 py-4 bg-slate-900 text-white flex items-center justify-between">
          <div className="flex items-center space-x-2.5">
            <Activity className="w-5 h-5 text-emerald-400" />
            <div>
              <h3 className="font-bold text-sm tracking-wide">Record Clinical Checkup</h3>
              <p className="text-[11px] text-slate-300">Patient: {patient.full_name} ({patient.patient_code})</p>
            </div>
          </div>
          <button onClick={onClose} className="p-1 text-slate-400 hover:text-white rounded-lg">
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Form Body */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {error && (
            <div className="p-3 rounded-xl bg-rose-50 text-rose-700 text-xs font-semibold border border-rose-200">
              {error}
            </div>
          )}

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Systolic BP (mmHg)</label>
              <input
                type="number"
                min="60"
                max="240"
                required
                value={formData.systolic_bp}
                onChange={(e) => setFormData({ ...formData, systolic_bp: Number(e.target.value) })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Diastolic BP (mmHg)</label>
              <input
                type="number"
                min="40"
                max="140"
                required
                value={formData.diastolic_bp}
                onChange={(e) => setFormData({ ...formData, diastolic_bp: Number(e.target.value) })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Fasting Glucose (mg/dL)</label>
              <input
                type="number"
                min="50"
                max="400"
                step="0.1"
                required
                value={formData.fasting_glucose}
                onChange={(e) => setFormData({ ...formData, fasting_glucose: Number(e.target.value) })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Total Cholesterol (mg/dL)</label>
              <input
                type="number"
                min="80"
                max="450"
                step="0.1"
                required
                value={formData.total_cholesterol}
                onChange={(e) => setFormData({ ...formData, total_cholesterol: Number(e.target.value) })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Body Mass Index (BMI)</label>
              <input
                type="number"
                min="12"
                max="60"
                step="0.1"
                required
                value={formData.bmi}
                onChange={(e) => setFormData({ ...formData, bmi: Number(e.target.value) })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-bold text-slate-700 mb-1">Exercise (Hours/Week)</label>
              <input
                type="number"
                min="0"
                max="25"
                step="0.5"
                value={formData.physical_activity_hours}
                onChange={(e) => setFormData({ ...formData, physical_activity_hours: Number(e.target.value) })}
                className="w-full px-3.5 py-2 border border-slate-200 rounded-xl text-xs focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="flex items-center space-x-6 pt-2">
            <label className="flex items-center space-x-2 text-xs font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.smoking_status}
                onChange={(e) => setFormData({ ...formData, smoking_status: e.target.checked })}
                className="rounded-sm border-slate-300 text-blue-600 focus:ring-blue-500"
              />
              <span>Current Tobacco Smoker</span>
            </label>
            <label className="flex items-center space-x-2 text-xs font-semibold text-slate-700 cursor-pointer">
              <input
                type="checkbox"
                checked={formData.alcohol_consumption}
                onChange={(e) => setFormData({ ...formData, alcohol_consumption: e.target.checked })}
                className="rounded-sm border-slate-300 text-blue-600 focus:ring-blue-500"
              />
              <span>Alcohol Consumer</span>
            </label>
          </div>

          <div className="pt-2 flex justify-end space-x-2.5">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:bg-slate-100 rounded-xl"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-5 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 rounded-xl shadow-md shadow-emerald-600/20 flex items-center space-x-1.5"
            >
              <Save className="w-3.5 h-3.5" />
              <span>{loading ? 'Recording...' : 'Record & Run AI Diagnosis'}</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

