import React from 'react';
import { 
  Activity, 
  Users, 
  Gauge, 
  SlidersHorizontal, 
  BarChart3, 
  FileText, 
  LogOut, 
  ShieldCheck,
  Stethoscope
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, currentDoctor, onLogout }) {
  const menuItems = [
    { id: 'dashboard', label: 'Clinical Overview', icon: Activity },
    { id: 'patients', label: 'Patient Directory', icon: Users },
    { id: 'diagnostics', label: 'DataVision Risk AI', icon: Gauge },
    { id: 'what-if', label: 'What-If Lifestyle Lab', icon: SlidersHorizontal },
    { id: 'population', label: 'Population Analytics', icon: BarChart3 },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-100 flex flex-col h-screen fixed left-0 top-0 border-r border-slate-800 z-30 select-none">
      {/* Brand Header */}
      <div className="p-6 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
          <Stethoscope className="w-5 h-5 text-white" />
        </div>
        <div>
          <h1 className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-cyan-400 bg-clip-text text-transparent">
            DataVision
          </h1>
          <p className="text-xs text-cyan-400/80 font-medium tracking-wide">
            HEALTH OBSERVATORY
          </p>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-4 py-6 space-y-1.5 overflow-y-auto">
        <div className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider px-3 mb-2">
          Diagnostic Suite
        </div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/30 font-semibold'
                  : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Doctor Profile Footer */}
      <div className="p-4 border-t border-slate-800 bg-slate-900/80">
        <div className="flex items-center space-x-3 p-2 rounded-lg bg-slate-800/50">
          <div className="w-8 h-8 rounded-full bg-blue-500/20 text-blue-400 flex items-center justify-center font-bold text-xs border border-blue-500/30">
            DR
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-xs font-semibold text-slate-200 truncate">
              {currentDoctor?.full_name || 'Dr. Eleanor Vance'}
            </p>
            <p className="text-[10px] text-emerald-400 flex items-center space-x-1">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Online Clinician</span>
            </p>
          </div>
          <button
            onClick={onLogout}
            title="Log Out"
            className="p-1.5 text-slate-400 hover:text-rose-400 hover:bg-slate-700/50 rounded-md transition-colors"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}

