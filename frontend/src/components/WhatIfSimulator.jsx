import React, { useState, useEffect } from 'react';
import { Sliders, Sparkles, ArrowRight, ShieldCheck, TrendingDown, RefreshCw } from 'lucide-react';
import { api } from '../services/api';
import RiskGauge from './RiskGauge';

export default function WhatIfSimulator({ patient, onApplyToPatient }) {
  const initialBaseline = {
    age: patient?.age || 52,
    gender: patient?.gender || 'Male',
    systolic_bp: patient?.latest_vitals?.systolic_bp || 142,
    diastolic_bp: patient?.latest_vitals?.diastolic_bp || 90,
    fasting_glucose: patient?.latest_vitals?.fasting_glucose || 128,
    total_cholesterol: patient?.latest_vitals?.total_cholesterol || 215,
    bmi: patient?.latest_vitals?.bmi || 28.5,
    smoking_status: patient?.latest_vitals?.smoking_status || true,
    physical_activity_hours: 2.0,
  };

  const [baseline, setBaseline] = useState(initialBaseline);
  const [params, setParams] = useState({
    systolic_bp: initialBaseline.systolic_bp,
    fasting_glucose: initialBaseline.fasting_glucose,
    bmi: initialBaseline.bmi,
    smoking_status: initialBaseline.smoking_status,
    physical_activity_hours: initialBaseline.physical_activity_hours,
  });

  const [simulationResult, setSimulationResult] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    runSimulation();
  }, [params]);

  const runSimulation = async () => {
    setLoading(true);
    try {
      const res = await api.simulateWhatIf(baseline, params);
      setSimulationResult(res);
    } catch (err) {
      console.error('Simulation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const resetToBaseline = () => {
    setParams({
      systolic_bp: baseline.systolic_bp,
      fasting_glucose: baseline.fasting_glucose,
      bmi: baseline.bmi,
      smoking_status: baseline.smoking_status,
      physical_activity_hours: baseline.physical_activity_hours,
    });
  };

  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 rounded-3xl p-6 text-white shadow-xl">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/20 text-cyan-300 text-xs font-semibold mb-2 border border-blue-400/30">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Interactive Lifestyle Simulation Lab (4 Diseases)</span>
            </div>
            <h2 className="text-xl font-bold tracking-tight">
              What-If Counterfactual Prognosis
            </h2>
            <p className="text-xs text-slate-300 mt-1 max-w-xl">
              Dynamically manipulate therapeutic targets and lifestyle levers (BP reduction, weight loss, glycemic control, tobacco cessation) to quantify risk reduction in real time across cardiometabolic and renal diseases.
            </p>
          </div>
          <button
            onClick={resetToBaseline}
            className="self-start md:self-auto flex items-center space-x-2 px-4 py-2 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-xs font-semibold transition-all border border-slate-700"
          >
            <RefreshCw className="w-3.5 h-3.5" />
            <span>Reset to Baseline</span>
          </button>
        </div>
      </div>

      {/* Simulator Controls & Real-Time Output Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Sliders Panel (5 columns) */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs space-y-5">
          <h3 className="font-bold text-slate-800 text-sm flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-blue-600" />
            <span>Therapeutic & Lifestyle Adjustments</span>
          </h3>

          {/* SBP Slider */}
          <div>
            <div className="flex justify-between text-xs font-medium mb-1.5">
              <span className="text-slate-700">Target Systolic BP</span>
              <span className="font-mono font-bold text-blue-600">{params.systolic_bp} mmHg</span>
            </div>
            <input
              type="range"
              min="90"
              max="180"
              step="2"
              value={params.systolic_bp}
              onChange={(e) => setParams({ ...params, systolic_bp: Number(e.target.value) })}
              className="w-full accent-blue-600 cursor-pointer h-2 bg-slate-100 rounded-lg"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>90 mmHg (Optimal)</span>
              <span>180 mmHg (Severe)</span>
            </div>
          </div>

          {/* Fasting Glucose Slider */}
          <div>
            <div className="flex justify-between text-xs font-medium mb-1.5">
              <span className="text-slate-700">Target Fasting Glucose</span>
              <span className="font-mono font-bold text-blue-600">{params.fasting_glucose} mg/dL</span>
            </div>
            <input
              type="range"
              min="70"
              max="240"
              step="2"
              value={params.fasting_glucose}
              onChange={(e) => setParams({ ...params, fasting_glucose: Number(e.target.value) })}
              className="w-full accent-blue-600 cursor-pointer h-2 bg-slate-100 rounded-lg"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>70 mg/dL (Normal)</span>
              <span>240 mg/dL (Diabetic)</span>
            </div>
          </div>

          {/* BMI Slider */}
          <div>
            <div className="flex justify-between text-xs font-medium mb-1.5">
              <span className="text-slate-700">Target BMI</span>
              <span className="font-mono font-bold text-blue-600">{params.bmi} kg/m²</span>
            </div>
            <input
              type="range"
              min="18.5"
              max="42.0"
              step="0.5"
              value={params.bmi}
              onChange={(e) => setParams({ ...params, bmi: Number(e.target.value) })}
              className="w-full accent-blue-600 cursor-pointer h-2 bg-slate-100 rounded-lg"
            />
            <div className="flex justify-between text-[10px] text-slate-400 mt-0.5">
              <span>18.5 (Lean)</span>
              <span>42.0 (Obese Cl. III)</span>
            </div>
          </div>

          {/* Physical Activity Slider */}
          <div>
            <div className="flex justify-between text-xs font-medium mb-1.5">
              <span className="text-slate-700">Weekly Exercise Hours</span>
              <span className="font-mono font-bold text-blue-600">{params.physical_activity_hours} hrs/wk</span>
            </div>
            <input
              type="range"
              min="0"
              max="12"
              step="0.5"
              value={params.physical_activity_hours}
              onChange={(e) => setParams({ ...params, physical_activity_hours: Number(e.target.value) })}
              className="w-full accent-blue-600 cursor-pointer h-2 bg-slate-100 rounded-lg"
            />
          </div>

          {/* Tobacco Smoking Toggle */}
          <div className="pt-2 border-t border-slate-100 flex items-center justify-between">
            <span className="text-xs font-medium text-slate-700">Smoking Cessation</span>
            <button
              type="button"
              onClick={() => setParams({ ...params, smoking_status: !params.smoking_status })}
              className={`px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                !params.smoking_status
                  ? 'bg-emerald-100 text-emerald-800 border border-emerald-300'
                  : 'bg-rose-100 text-rose-800 border border-rose-300'
              }`}
            >
              {!params.smoking_status ? '✓ Tobacco Free' : '✗ Active Tobacco User'}
            </button>
          </div>
        </div>

        {/* Real-time Prognosis Output (7 columns) */}
        <div className="lg:col-span-7 space-y-4">
          {simulationResult && (
            <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs">
              <div className="flex items-center justify-between mb-4">
                <h3 className="font-bold text-slate-800 text-sm">
                  Simulated Prognosis vs Baseline Comparison
                </h3>
                <div className="text-xs font-bold text-blue-600 bg-blue-50 px-3 py-1 rounded-full border border-blue-200">
                  Overall Health Score: {simulationResult.simulated_health_score}/100
                </div>
              </div>

              {/* 4 Disease Comparison Cards */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
                {Object.keys(simulationResult.simulated_risks).map((key) => {
                  const base = simulationResult.baseline_risks[key];
                  const sim = simulationResult.simulated_risks[key];
                  const delta = simulationResult.risk_delta[key] !== undefined ? simulationResult.risk_delta[key] : (sim.risk_percentage - base.risk_percentage);
                  const isImproved = delta <= 0;

                  return (
                    <div
                      key={key}
                      className="bg-slate-50/80 rounded-xl p-4 border border-slate-200/80 flex flex-col justify-between"
                    >
                      <div>
                        <div className="text-xs font-bold text-slate-700 mb-1">{sim.disease_type}</div>
                        <div className="flex items-baseline space-x-2">
                          <span className="text-xl font-black text-slate-900">{sim.risk_percentage}%</span>
                          <span className="text-xs text-slate-400 line-through">
                            {base.risk_percentage}%
                          </span>
                        </div>
                      </div>

                      <div className="mt-3 pt-2 border-t border-slate-200/60 flex items-center justify-between">
                        <span className="text-[10px] font-semibold text-slate-500">Net Shift</span>
                        <span
                          className={`text-xs font-bold px-2 py-0.5 rounded-md ${
                            isImproved
                              ? 'bg-emerald-100 text-emerald-700'
                              : 'bg-rose-100 text-rose-700'
                          }`}
                        >
                          {delta > 0 ? `+${delta}%` : `${delta}%`}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>

              <div className="mt-5 p-4 rounded-xl bg-cyan-50/70 border border-cyan-200 flex items-start space-x-3 text-xs text-cyan-900">
                <ShieldCheck className="w-5 h-5 text-cyan-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Multisystem Protective Synergy:</span> Attaining normal hemodynamics (BP &lt; 125 mmHg) and glycemic stabilization produces compounded protective benefits across both renal filtration microvasculature and coronary arteries.
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
