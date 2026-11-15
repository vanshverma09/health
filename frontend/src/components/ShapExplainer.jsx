import React from 'react';
import { HelpCircle, AlertTriangle, ShieldCheck } from 'lucide-react';

export default function ShapExplainer({ featureContributions, diseaseTitle }) {
  if (!featureContributions || featureContributions.length === 0) {
    return (
      <div className="bg-white rounded-2xl p-6 border border-slate-200 text-center text-slate-400 text-sm">
        No explainability metrics available for this diagnostic run.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="font-bold text-slate-800 text-base">
            Explainable AI (XAI) Biomarker Attributions
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Individual biomarker impact on {diseaseTitle || 'condition'} prediction
          </p>
        </div>
        <div className="flex items-center space-x-3 text-[11px] font-semibold">
          <span className="flex items-center space-x-1 text-rose-600">
            <span className="w-2.5 h-2.5 rounded-sm bg-rose-500"></span>
            <span>Increases Risk</span>
          </span>
          <span className="flex items-center space-x-1 text-emerald-600">
            <span className="w-2.5 h-2.5 rounded-sm bg-emerald-500"></span>
            <span>Protective (Decreases Risk)</span>
          </span>
        </div>
      </div>

      {/* Feature attribution bars */}
      <div className="space-y-3.5 mt-5">
        {featureContributions.map((item, idx) => {
          const impact = item.impact_score; // e.g. +0.22 or -0.15
          const isPositiveRisk = impact > 0;
          const absImpact = Math.min(100, Math.abs(impact * 180)); // scaled for visual bar width

          return (
            <div key={idx} className="group">
              <div className="flex justify-between items-center text-xs mb-1">
                <div className="flex items-center space-x-1.5 font-medium text-slate-700">
                  {isPositiveRisk ? (
                    <AlertTriangle className="w-3.5 h-3.5 text-rose-500" />
                  ) : (
                    <ShieldCheck className="w-3.5 h-3.5 text-emerald-500" />
                  )}
                  <span>{item.label}</span>
                  <span className="text-slate-400 font-normal">
                    (Patient: {item.patient_value} | Ref: {item.baseline_value})
                  </span>
                </div>
                <span
                  className={`font-mono font-bold text-xs ${
                    isPositiveRisk ? 'text-rose-600' : 'text-emerald-600'
                  }`}
                >
                  {isPositiveRisk ? `+${(impact * 100).toFixed(1)}%` : `${(impact * 100).toFixed(1)}%`}
                </span>
              </div>

              {/* Center-aligned diverging bar */}
              <div className="h-2.5 bg-slate-100 rounded-full overflow-hidden flex relative">
                {/* Center dividing tick */}
                <div className="absolute left-1/2 top-0 bottom-0 w-0.5 bg-slate-300 z-10"></div>

                {/* Left side (Protective) */}
                <div className="w-1/2 flex justify-end">
                  {!isPositiveRisk && (
                    <div
                      style={{ width: `${absImpact}%` }}
                      className="h-full bg-emerald-500 rounded-l-full transition-all duration-500 ease-out"
                    ></div>
                  )}
                </div>

                {/* Right side (Risk Driver) */}
                <div className="w-1/2 flex justify-start">
                  {isPositiveRisk && (
                    <div
                      style={{ width: `${absImpact}%` }}
                      className="h-full bg-rose-500 rounded-r-full transition-all duration-500 ease-out"
                    ></div>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

