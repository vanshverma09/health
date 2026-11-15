import React, { useState, useEffect } from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  PieChart, 
  Pie, 
  Cell,
  Legend
} from 'recharts';
import { BarChart3, Users, AlertTriangle, ShieldCheck, PieChart as PieIcon } from 'lucide-react';
import { api } from '../services/api';

export default function PopulationAnalytics() {
  const [cohortData, setCohortData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCohort();
  }, []);

  const fetchCohort = async () => {
    try {
      setLoading(true);
      const data = await api.getCohortAnalytics();
      setCohortData(data);
    } catch (err) {
      console.error('Failed to load cohort analytics:', err);
    } finally {
      setLoading(false);
    }
  };

  // Age group chart formatting
  const ageChartData = cohortData?.age_groups
    ? Object.entries(cohortData.age_groups).map(([group, count]) => ({
        ageGroup: group,
        patients: count,
      }))
    : [];

  // Risk distribution chart formatting
  const riskColors = {
    LOW: '#10b981',
    MODERATE: '#f59e0b',
    HIGH: '#f97316',
    CRITICAL: '#ef4444',
  };

  const riskPieData = cohortData?.risk_distribution
    ? Object.entries(cohortData.risk_distribution).map(([level, count]) => ({
        name: level,
        value: count,
        color: riskColors[level] || '#64748b',
      }))
    : [];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 rounded-3xl p-6 sm:p-8 text-white shadow-xl">
        <div className="flex items-center space-x-2 text-xs text-indigo-300 font-semibold mb-2">
          <BarChart3 className="w-4 h-4" />
          <span>Epidemiological Cohort Analytics</span>
        </div>
        <h2 className="text-xl sm:text-2xl font-bold tracking-tight">
          Hospital Population Health Observatory
        </h2>
        <p className="text-xs sm:text-sm text-slate-300 mt-1 max-w-2xl">
          Aggregated risk distribution across demographic age bands and chronic disease prevalence metrics.
        </p>
      </div>

      {/* Main Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Age Demographics Bar Chart (7 cols) */}
        <div className="lg:col-span-7 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs">
          <h3 className="font-bold text-slate-800 text-sm mb-1">
            Patient Age Demographics Distribution
          </h3>
          <p className="text-xs text-slate-400 mb-6">Cohort distribution across age cohorts</p>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={ageChartData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="ageGroup" stroke="#94a3b8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#0f172a',
                    color: '#f8fafc',
                    borderRadius: '10px',
                    border: 'none',
                    fontSize: '12px'
                  }}
                />
                <Bar dataKey="patients" name="Patient Count" fill="#3b82f6" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Risk Distribution Donut Chart (5 cols) */}
        <div className="lg:col-span-5 bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs flex flex-col justify-between">
          <div>
            <h3 className="font-bold text-slate-800 text-sm mb-1">
              Cohort Risk Stratification
            </h3>
            <p className="text-xs text-slate-400 mb-4">Proportion of patients across clinical risk tiers</p>

            <div className="h-56 w-full flex items-center justify-center">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={riskPieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={75}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {riskPieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#0f172a',
                      color: '#f8fafc',
                      borderRadius: '10px',
                      border: 'none',
                      fontSize: '12px'
                    }}
                  />
                  <Legend wrapperStyle={{ fontSize: '11px' }} />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 grid grid-cols-2 gap-2 text-center text-xs">
            <div className="p-2 rounded-xl bg-emerald-50 text-emerald-800 font-semibold">
              Low / Moderate: Stable
            </div>
            <div className="p-2 rounded-xl bg-rose-50 text-rose-800 font-semibold">
              High / Critical: Priority
            </div>
          </div>
        </div>
      </div>

      {/* Disease Prevalence Cards */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs">
        <h3 className="font-bold text-slate-800 text-sm mb-4">
          Chronic Disease Prevalence & High Risk Incidence
        </h3>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {cohortData?.disease_prevalence?.map((d) => (
            <div
              key={d.disease}
              className="p-4 rounded-xl border border-slate-200/80 bg-slate-50/50 flex flex-col justify-between"
            >
              <div>
                <span className="text-xs font-bold text-slate-700">{d.disease}</span>
                <div className="flex items-baseline space-x-2 mt-1">
                  <span className="text-2xl font-black text-slate-900">{d.prevalence_rate}%</span>
                  <span className="text-xs text-slate-400">cohort rate</span>
                </div>
              </div>
              <div className="mt-3 text-[11px] font-semibold text-rose-600 bg-rose-50 px-2.5 py-1 rounded-lg self-start">
                {d.high_risk_cases} High Risk Individuals
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

