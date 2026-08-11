'use client';

import React, { useState, useEffect } from 'react';
import { sendTestEmail, triggerDailyDigest, getLatestProfile } from '@/lib/api';
import { Mail, Send, CheckCircle2, AlertCircle, Loader2, Sparkles } from 'lucide-react';

export default function EmailAlertForm() {
  const [email, setEmail] = useState('');
  const [sendingTest, setSendingTest] = useState(false);
  const [triggeringDigest, setTriggeringDigest] = useState(false);

  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function loadCandidateEmail() {
      const profile = await getLatestProfile();
      if (profile && profile.profile_data.email) {
        setEmail(profile.profile_data.email);
      }
    }
    loadCandidateEmail();
  }, []);

  const handleTestEmail = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email) {
      setError('Please enter a recipient email address.');
      return;
    }

    setSendingTest(true);
    setMessage(null);
    setError(null);

    try {
      const res = await sendTestEmail(email);
      setMessage(`Test HTML Email Digest successfully dispatched to ${email}!`);
    } catch (err: any) {
      setError(err.message || 'Failed to send test email digest');
    } finally {
      setSendingTest(false);
    }
  };

  const handleTriggerLiveDigest = async () => {
    if (!email) {
      setError('Please enter a recipient email address.');
      return;
    }

    setTriggeringDigest(true);
    setMessage(null);
    setError(null);

    try {
      const res = await triggerDailyDigest(email);
      setMessage(
        `Live Daily Digest executed! Ingested ${res.jobs_ingested || 0} jobs, evaluated ${res.jobs_matched || 0} matches, and dispatched top ${res.top_matches_found || 0} jobs to ${email}.`
      );
    } catch (err: any) {
      setError(err.message || 'Failed to trigger live daily digest');
    } finally {
      setTriggeringDigest(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div className="p-8 rounded-2xl bg-slate-850/70 border border-slate-800 space-y-6 shadow-xl">
        <div className="flex items-center gap-3 border-b border-slate-800 pb-4">
          <div className="p-2.5 rounded-xl bg-brand-500/20 text-brand-400 border border-brand-500/30">
            <Mail className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-lg font-bold text-white">Daily Email Digest Alerts</h2>
            <p className="text-xs text-slate-400">
              Receive your personalized "YOUR AI JOB DIGEST" featuring your top matched jobs, match percentage badges, and direct apply links.
            </p>
          </div>
        </div>

        <form onSubmit={handleTestEmail} className="space-y-4">
          <div className="space-y-1.5">
            <label className="block text-xs font-semibold text-slate-300">Recipient Email Address</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="e.g. yourname@example.com"
              required
              className="w-full px-4 py-3 rounded-xl bg-slate-800 border border-slate-700 text-white font-medium text-sm focus:outline-none focus:border-brand-500"
            />
          </div>

          <div className="pt-2 flex flex-col sm:flex-row items-center gap-4">
            <button
              type="submit"
              disabled={sendingTest || triggeringDigest}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-200 font-semibold text-xs border border-slate-700 flex items-center justify-center gap-2 shadow-sm transition-all"
            >
              {sendingTest ? <Loader2 className="w-4 h-4 animate-spin" /> : <Mail className="w-4 h-4" />}
              <span>Send Sample Test Digest Email</span>
            </button>

            <button
              type="button"
              onClick={handleTriggerLiveDigest}
              disabled={sendingTest || triggeringDigest}
              className="w-full sm:w-auto px-6 py-3 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-semibold text-xs flex items-center justify-center gap-2 shadow-lg shadow-brand-500/20 transition-all"
            >
              {triggeringDigest ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
              <span>Send Live Daily AI Job Digest</span>
            </button>
          </div>
        </form>

        {error && (
          <div className="p-4 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-xs flex items-center gap-2">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {message && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 flex-shrink-0" />
            <span>{message}</span>
          </div>
        )}
      </div>
    </div>
  );
}
