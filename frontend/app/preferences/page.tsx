import PreferenceForm from '@/components/PreferenceForm';
import { Sliders } from 'lucide-react';

export default function PreferencesPage() {
  return (
    <div className="space-y-8">
      <div className="space-y-2 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
          <Sliders className="w-4 h-4" />
          <span>Job Search Settings</span>
        </div>
        <h1 className="text-3xl font-bold text-white">Candidate Job Preferences</h1>
        <p className="text-sm text-slate-400">
          Configure your location preferences, work modes (Remote India/Worldwide, Hybrid), preferred tech hub cities, and minimum AI match threshold.
        </p>
      </div>

      <PreferenceForm />
    </div>
  );
}
