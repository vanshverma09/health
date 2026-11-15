import React, { useState } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ReferenceLine
} from 'recharts';
import { Calendar, TrendingUp, AlertCircle } from 'lucide-react';

export default function VitalsTimeline({ records }) {
  const [selectedMetric, setSelectedMetric] = useState('all');

  if (!records || records.length === 0) {
    return (
      <div className="bg-white rounded-2xl p-8 border border-slate-200/80 text-center text-slate-400">
        <AlertCircle className="w-8 h-8 mx-auto mb-2 text-slate-300" />
        <p className="font-medium text-sm">No longitudinal records found for this patient.</p>
        <p className="text-xs text-slate-400 mt-1">Add initial vital checkups to view trends over time.</p>
      </div>
    );
  }

  // Format data for Recharts
  const chartData = records.map((rec) => ({
    date: new Date(rec.recorded_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    fullDate: new Date(rec.recorded_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }),
    systolic_bp: rec.systolic_bp,
    diastolic_bp: rec.diastolic_bp,
    glucose: rec.fasting_glucose,
    bmi: rec.bmi,
    cholesterol: rec.total_cholesterol,
  }));

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200/80 shadow-xs">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
        <div>
          <h3 className="font-bold text-slate-800 text-base flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            <span>Longitudinal Biomarker Trajectory</span>
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Historical patient clinical trends plotted across {records.length} consultation visits
          </p>
        </div>

        {/* Metric Switcher Tabs */}
        <div className="flex bg-slate-100 p-1 rounded-xl text-xs font-semibold text-slate-600">
          <button
            onClick={() => setSelectedMetric('all')}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedMetric === 'all' ? 'bg-white text-blue-600 shadow-xs' : 'hover:text-slate-900'
            }`}
          >
            All Vitals
          </button>
          <button
            onClick={() => setSelectedMetric('bp')}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedMetric === 'bp' ? 'bg-white text-blue-600 shadow-xs' : 'hover:text-slate-900'
            }`}
          >
            Blood Pressure
          </button>
          <button
            onClick={() => setSelectedMetric('glucose')}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedMetric === 'glucose' ? 'bg-white text-blue-600 shadow-xs' : 'hover:text-slate-900'
            }`}
          >
            Glucose
          </button>
          <button
            onClick={() => setSelectedMetric('bmi')}
            className={`px-3 py-1.5 rounded-lg transition-all ${
              selectedMetric === 'bmi' ? 'bg-white text-blue-600 shadow-xs' : 'hover:text-slate-900'
            }`}
          >
            BMI
          </button>
        </div>
      </div>

      {/* Recharts Timeline Area */}
      <div className="h-72 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
            <XAxis dataKey="date" stroke="#94a3b8" fontSize={11} tickLine={false} />
            <YAxis stroke="#94a3b8" fontSize={11} tickLine={false} />
            <Tooltip
              contentStyle={{
                backgroundColor: '#0f172a',
                color: '#f8fafc',
                borderRadius: '12px',
                border: 'none',
                boxShadow: '0 10px 15px -3px rgba(0,0,0,0.2)',
                fontSize: '12px'
              }}
              labelFormatter={(label, payload) => {
                const item = payload?.[0]?.payload;
                return item ? `Consultation: ${item.fullDate}` : label;
              }}
            />
            <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />

            {/* Reference clinical thresholds */}
            {selectedMetric === 'bp' && (
              <ReferenceLine y={120} stroke="#10b981" strokeDasharray="4 4" label={{ value: 'Target SBP 120', fill: '#10b981', fontSize: 10 }} />
            )}
            {selectedMetric === 'glucose' && (
              <ReferenceLine y={100} stroke="#10b981" strokeDasharray="4 4" label={{ value: 'Fasting Normal < 100', fill: '#10b981', fontSize: 10 }} />
            )}
            {selectedMetric === 'bmi' && (
              <ReferenceLine y={25} stroke="#10b981" strokeDasharray="4 4" label={{ value: 'Normal BMI < 25', fill: '#10b981', fontSize: 10 }} />
            )}

            {/* Render lines based on selected filter */}
            {(selectedMetric === 'all' || selectedMetric === 'bp') && (
              <>
                <Line
                  type="monotone"
                  dataKey="systolic_bp"
                  name="Systolic BP (mmHg)"
                  stroke="#ef4444"
                  strokeWidth={2.5}
                  dot={{ r: 4, fill: '#ef4444' }}
                  activeDot={{ r: 6 }}
                />
                <Line
                  type="monotone"
                  dataKey="diastolic_bp"
                  name="Diastolic BP (mmHg)"
                  stroke="#f97316"
                  strokeWidth={2}
                  dot={{ r: 3, fill: '#f97316' }}
                />
              </>
            )}

            {(selectedMetric === 'all' || selectedMetric === 'glucose') && (
              <Line
                type="monotone"
                dataKey="glucose"
                name="Fasting Glucose (mg/dL)"
                stroke="#3b82f6"
                strokeWidth={2.5}
                dot={{ r: 4, fill: '#3b82f6' }}
                activeDot={{ r: 6 }}
              />
            )}

            {(selectedMetric === 'all' || selectedMetric === 'bmi') && (
              <Line
                type="monotone"
                dataKey="bmi"
                name="BMI (kg/m²)"
                stroke="#8b5cf6"
                strokeWidth={2}
                dot={{ r: 3, fill: '#8b5cf6' }}
              />
            )}

            {selectedMetric === 'all' && (
              <Line
                type="monotone"
                dataKey="cholesterol"
                name="Total Cholesterol (mg/dL)"
                stroke="#06b6d4"
                strokeWidth={2}
                strokeDasharray="5 5"
                dot={{ r: 3, fill: '#06b6d4' }}
              />
            )}
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

