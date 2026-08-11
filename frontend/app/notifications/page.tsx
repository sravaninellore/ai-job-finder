import EmailAlertForm from '@/components/EmailAlertForm';
import { Mail } from 'lucide-react';

export default function NotificationsPage() {
  return (
    <div className="space-y-8">
      <div className="space-y-2 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
          <Mail className="w-4 h-4" />
          <span>Email Digest Alerts</span>
        </div>
        <h1 className="text-3xl font-bold text-white">Email Digest Alert Mechanism</h1>
        <p className="text-sm text-slate-400">
          Configure your daily email digest recipient and test email alerts directly from your dashboard.
        </p>
      </div>

      <EmailAlertForm />
    </div>
  );
}
