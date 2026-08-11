'use client';

import React from 'react';

interface JobFiltersProps {
  workMode: string;
  setWorkMode: (v: string) => void;
  remoteScope: string;
  setRemoteScope: (v: string) => void;
  source: string;
  setSource: (v: string) => void;
  minScore: number;
  setMinScore: (v: number) => void;
}

const SOURCES = [
  { id: '', name: 'All 13 Sources' },
  { id: 'instahyre', name: '⚡ Instahyre' },
  { id: 'internshala', name: '🎓 Internshala' },
  { id: 'naukri', name: '🇮🇳 Naukri India' },
  { id: 'linkedin', name: '💼 LinkedIn' },
  { id: 'wellfound', name: '🚀 Wellfound' },
  { id: 'foundit', name: '🇮🇳 Foundit' },
  { id: 'greenhouse', name: '🟢 Greenhouse ATS' },
  { id: 'lever', name: '🔷 Lever ATS' },
  { id: 'ashby', name: '⚡ Ashby ATS' },
  { id: 'remoteok', name: '🌍 RemoteOK' },
  { id: 'weworkremotely', name: '📡 WeWorkRemotely' },
  { id: 'indeed', name: '🔍 Indeed' },
  { id: 'glassdoor', name: '📊 Glassdoor' },
];

export default function JobFilters({
  workMode,
  setWorkMode,
  remoteScope,
  setRemoteScope,
  source,
  setSource,
  minScore,
  setMinScore,
}: JobFiltersProps) {
  return (
    <div className="p-4 rounded-2xl bg-slate-850/60 border border-slate-800 flex flex-wrap items-center justify-between gap-4 text-xs">
      <div className="flex flex-wrap items-center gap-4">
        {/* Job Source Filter */}
        <div className="space-y-1">
          <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Job Source
          </label>
          <select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 focus:outline-none focus:border-brand-500 cursor-pointer font-medium"
          >
            {SOURCES.map((s) => (
              <option key={s.id} value={s.id}>
                {s.name}
              </option>
            ))}
          </select>
        </div>

        {/* Work Mode Filter */}
        <div className="space-y-1">
          <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Work Mode
          </label>
          <select
            value={workMode}
            onChange={(e) => setWorkMode(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 focus:outline-none focus:border-brand-500 cursor-pointer"
          >
            <option value="">All Work Modes</option>
            <option value="REMOTE">Remote Only</option>
            <option value="HYBRID">Hybrid Only</option>
            <option value="ONSITE">On-Site Only</option>
          </select>
        </div>

        {/* Remote Scope Filter */}
        <div className="space-y-1">
          <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Remote Scope
          </label>
          <select
            value={remoteScope}
            onChange={(e) => setRemoteScope(e.target.value)}
            className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 focus:outline-none focus:border-brand-500 cursor-pointer"
          >
            <option value="">All Scopes</option>
            <option value="INDIA">India Remote</option>
            <option value="WORLDWIDE">Worldwide Remote</option>
            <option value="US_ONLY">US Only</option>
          </select>
        </div>

        {/* Min Score Filter */}
        <div className="space-y-1">
          <label className="block text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
            Min Match Score: <strong className="text-brand-400">{minScore}%</strong>
          </label>
          <input
            type="range"
            min="0"
            max="95"
            step="5"
            value={minScore}
            onChange={(e) => setMinScore(Number(e.target.value))}
            className="w-32 accent-brand-500 cursor-pointer"
          />
        </div>
      </div>
    </div>
  );
}
