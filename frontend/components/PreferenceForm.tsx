'use client';

import React, { useState, useEffect } from 'react';
import { CandidatePreference, getPreferences, updatePreferences } from '@/lib/api';
import { Sliders, Save, CheckCircle2, AlertCircle, MapPin, Globe, Building } from 'lucide-react';

export default function PreferenceForm() {
  const [pref, setPref] = useState<CandidatePreference>({
    allowed_work_modes: ['REMOTE', 'HYBRID', 'ONSITE'],
    allowed_remote_scopes: ['INDIA', 'WORLDWIDE'],
    preferred_cities: ['Bangalore', 'Hyderabad', 'Pune', 'Chennai'],
    allowed_employment_types: ['Full-time'],
    min_match_percentage: 70,
    max_experience_tolerance: 5,
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await getPreferences();
        setPref(data);
      } catch (err) {
        console.error('Error fetching preferences:', err);
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  const handleToggle = (key: keyof CandidatePreference, val: string) => {
    const list = (pref[key] as string[]) || [];
    const updated = list.includes(val) ? list.filter((item) => item !== val) : [...list, val];
    setPref({ ...pref, [key]: updated });
  };

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault();
    setSaving(true);
    setSuccess(false);
    setError(null);

    try {
      await updatePreferences(pref);
      setSuccess(true);
    } catch (err: any) {
      setError(err.message || 'Failed to save candidate preferences');
    } finally {
      setSaving(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-slate-400">Loading preferences...</div>;

  return (
    <form onSubmit={handleSave} className="space-y-8 max-w-3xl mx-auto">
      {/* Work Modes */}
      <div className="p-6 rounded-2xl bg-slate-850/70 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-white">
          <Building className="w-4 h-4 text-brand-400" />
          <span>Work Modes Allowed</span>
        </div>
        <div className="flex flex-wrap gap-3">
          {['REMOTE', 'HYBRID', 'ONSITE'].map((mode) => {
            const checked = pref.allowed_work_modes.includes(mode);
            return (
              <button
                type="button"
                key={mode}
                onClick={() => handleToggle('allowed_work_modes', mode)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-all ${
                  checked
                    ? 'bg-brand-600/20 text-brand-300 border-brand-500/40 shadow-sm'
                    : 'bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-750'
                }`}
              >
                {mode === 'REMOTE' ? '☑ Remote' : mode === 'HYBRID' ? '☑ Hybrid' : '☑ On-site'}
              </button>
            );
          })}
        </div>
      </div>

      {/* Remote Scopes */}
      <div className="p-6 rounded-2xl bg-slate-850/70 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-white">
          <Globe className="w-4 h-4 text-indigo-400" />
          <span>Remote Scopes Allowed</span>
        </div>
        <div className="flex flex-wrap gap-3">
          {['INDIA', 'WORLDWIDE', 'US_ONLY'].map((scope) => {
            const checked = pref.allowed_remote_scopes.includes(scope);
            return (
              <button
                type="button"
                key={scope}
                onClick={() => handleToggle('allowed_remote_scopes', scope)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-all ${
                  checked
                    ? 'bg-indigo-600/20 text-indigo-300 border-indigo-500/40 shadow-sm'
                    : 'bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-750'
                }`}
              >
                {scope === 'INDIA'
                  ? '☑ Remote — India'
                  : scope === 'WORLDWIDE'
                  ? '☑ Remote — Worldwide'
                  : '⚠️ Remote — US Only'}
              </button>
            );
          })}
        </div>
      </div>

      {/* Preferred Indian Cities */}
      <div className="p-6 rounded-2xl bg-slate-850/70 border border-slate-800 space-y-4">
        <div className="flex items-center gap-2 text-sm font-semibold text-white">
          <MapPin className="w-4 h-4 text-emerald-400" />
          <span>Preferred Indian Cities (On-site / Hybrid)</span>
        </div>
        <div className="flex flex-wrap gap-3">
          {['Bangalore', 'Hyderabad', 'Pune', 'Chennai', 'Mumbai', 'Delhi NCR'].map((city) => {
            const checked = pref.preferred_cities.includes(city);
            return (
              <button
                type="button"
                key={city}
                onClick={() => handleToggle('preferred_cities', city)}
                className={`px-4 py-2 rounded-xl text-xs font-semibold border transition-all ${
                  checked
                    ? 'bg-emerald-600/20 text-emerald-300 border-emerald-500/40 shadow-sm'
                    : 'bg-slate-800 text-slate-400 border-slate-700 hover:bg-slate-750'
                }`}
              >
                {city}
              </button>
            );
          })}
        </div>
      </div>

      {/* Minimum Match Percentage Threshold */}
      <div className="p-6 rounded-2xl bg-slate-850/70 border border-slate-800 space-y-4">
        <div className="flex items-center justify-between">
          <label className="text-sm font-semibold text-white">Minimum AI Match Percentage</label>
          <span className="text-sm font-bold text-brand-400">{pref.min_match_percentage}%</span>
        </div>
        <input
          type="range"
          min="50"
          max="90"
          step="5"
          value={pref.min_match_percentage}
          onChange={(e) => setPref({ ...pref, min_match_percentage: Number(e.target.value) })}
          className="w-full accent-brand-500 cursor-pointer"
        />
        <p className="text-xs text-slate-400">
          Jobs scoring below {pref.min_match_percentage}% match will be filtered out from your digest.
        </p>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
          <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
          <span>Preferences updated successfully!</span>
        </div>
      )}

      <div className="flex justify-end pt-2">
        <button
          type="submit"
          disabled={saving}
          className="px-6 py-3 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-sm flex items-center gap-2 shadow-lg transition-all"
        >
          <Save className="w-4 h-4" />
          <span>{saving ? 'Saving...' : 'Save Job Preferences'}</span>
        </button>
      </div>
    </form>
  );
}
