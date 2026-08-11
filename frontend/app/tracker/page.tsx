import CRMBoard from '@/components/CRMBoard';
import { BookmarkCheck } from 'lucide-react';

export default function TrackerPage() {
  return (
    <div className="space-y-8">
      <div className="space-y-2 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
          <BookmarkCheck className="w-4 h-4" />
          <span>CRM Application Tracker</span>
        </div>
        <h1 className="text-3xl font-bold text-white">Job Search Pipeline Tracker</h1>
        <p className="text-sm text-slate-400">
          Track your application stages: New ➔ Saved ➔ Applied ➔ Screening ➔ Interview ➔ Offer
        </p>
      </div>

      <CRMBoard />
    </div>
  );
}
