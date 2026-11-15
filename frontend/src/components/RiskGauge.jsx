import React from 'react';

export default function RiskGauge({ percentage, level, diseaseName, subtitle }) {
  // SVG arc calculation for 180-degree semicircular gauge
  const radius = 68;
  const strokeWidth = 10;
  const circumference = Math.PI * radius; // half circle circumference
  const strokeDashoffset = circumference - (Math.min(100, Math.max(0, percentage)) / 100) * circumference;

  const getColor = (lvl) => {
    switch (lvl?.toUpperCase()) {
      case 'LOW':
        return { stroke: '#10b981', bg: 'bg-emerald-50 text-emerald-700 border-emerald-200' };
      case 'MODERATE':
        return { stroke: '#f59e0b', bg: 'bg-amber-50 text-amber-700 border-amber-200' };
      case 'HIGH':
        return { stroke: '#f97316', bg: 'bg-orange-50 text-orange-700 border-orange-200' };
      case 'CRITICAL':
        return { stroke: '#ef4444', bg: 'bg-rose-50 text-rose-700 border-rose-200' };
      default:
        return { stroke: '#64748b', bg: 'bg-slate-50 text-slate-700 border-slate-200' };
    }
  };

  const colorConfig = getColor(level);

  return (
    <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs hover:shadow-md transition-shadow flex flex-col items-center text-center relative overflow-hidden">
      {/* Top Header */}
      <div className="w-full flex items-center justify-between mb-2">
        <h3 className="font-bold text-sm text-slate-800 tracking-tight">{diseaseName}</h3>
        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${colorConfig.bg}`}>
          {level || 'EVALUATING'}
        </span>
      </div>
      {subtitle && <p className="text-[11px] text-slate-500 w-full text-left mb-3">{subtitle}</p>}

      {/* SVG Semicircle Gauge */}
      <div className="relative w-40 h-24 flex items-end justify-center my-2">
        <svg className="w-40 h-24 overflow-visible" viewBox="0 0 160 90">
          {/* Background track */}
          <path
            d="M 12 80 A 68 68 0 0 1 148 80"
            fill="none"
            stroke="#e2e8f0"
            strokeWidth={strokeWidth}
            strokeLinecap="round"
          />
          {/* Dynamic Fill Arc */}
          <path
            d="M 12 80 A 68 68 0 0 1 148 80"
            fill="none"
            stroke={colorConfig.stroke}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={strokeDashoffset}
            strokeLinecap="round"
            className="transition-all duration-700 ease-out"
          />
        </svg>

        {/* Center Percentage Display */}
        <div className="absolute bottom-1 flex flex-col items-center">
          <span className="text-2xl font-black text-slate-800 tracking-tight">
            {percentage !== undefined ? `${percentage}%` : '--'}
          </span>
          <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider">
            Risk Score
          </span>
        </div>
      </div>

      {/* Bottom Range Indicators */}
      <div className="w-full flex justify-between text-[10px] font-medium text-slate-400 px-3 mt-1">
        <span>0% (Safe)</span>
        <span>50%</span>
        <span>100% (Critical)</span>
      </div>
    </div>
  );
}

