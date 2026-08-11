'use client';

import React, { useState, useEffect } from 'react';
import { Job, updateJobStatus } from '@/lib/api';
import {
  ExternalLink,
  MapPin,
  Flame,
  CheckCircle2,
  Bookmark
} from 'lucide-react';

interface JobCardProps {
  job: Job;
  onStatusChange?: () => void;
}

export default function JobCard({ job, onStatusChange }: JobCardProps) {
  const [status, setStatus] = useState<string>(job.application_status || 'NEW');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (job.application_status) {
      setStatus(job.application_status);
    }
  }, [job.application_status]);

  const handleStatusUpdate = async (newStatus: string) => {
    setLoading(true);
    setStatus(newStatus);
    try {
      await updateJobStatus(job.id, newStatus);
      if (onStatusChange) onStatusChange();
    } catch (err) {
      console.error('Failed to update status:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyClick = () => {
    // Immediately update status dropdown to APPLIED
    if (status !== 'APPLIED') {
      setStatus('APPLIED');
      updateJobStatus(job.id, 'APPLIED')
        .then(() => {
          if (onStatusChange) onStatusChange();
        })
        .catch((err) => console.error('Failed to mark applied:', err));
    }
  };

  const getScoreColor = (score?: number) => {
    if (!score) return 'bg-slate-800 text-slate-400 border-slate-700';
    if (score >= 85) return 'bg-amber-500/15 text-amber-300 border-amber-500/30';
    if (score >= 70) return 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30';
    if (score >= 50) return 'bg-blue-500/15 text-blue-300 border-blue-500/30';
    return 'bg-red-500/15 text-red-300 border-red-500/30';
  };

  return (
    <div className="p-6 rounded-2xl bg-slate-850/70 border border-slate-800 hover:border-slate-700 transition-all duration-200 space-y-4 shadow-lg">
      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-4">
        <div className="space-y-1.5">
          <div className="flex items-center gap-2">
            <span className="text-xs font-semibold text-brand-400 uppercase tracking-wider">
              {job.company}
            </span>
            <span className="text-slate-600">•</span>
            <span className="text-xs text-slate-400 font-mono">{job.source}</span>
            {status === 'APPLIED' && (
              <span className="px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 text-[10px] font-bold border border-blue-500/30 flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3 text-blue-400" /> APPLIED
              </span>
            )}
            {status === 'SAVED' && (
              <span className="px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 text-[10px] font-bold border border-indigo-500/30 flex items-center gap-1">
                <Bookmark className="w-3 h-3 text-indigo-400" /> SAVED
              </span>
            )}
          </div>

          <h3 className="text-lg font-bold text-white leading-snug">{job.title}</h3>

          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-400 pt-1">
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-indigo-400" />
              {job.location || job.city || 'Remote'}
            </span>
            <span>•</span>
            <span className="px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 text-[11px] font-semibold border border-slate-700">
              {job.work_mode}
            </span>
            {job.remote_scope && (
              <span className="px-2 py-0.5 rounded-md bg-indigo-500/10 text-indigo-300 text-[11px] font-semibold border border-indigo-500/20">
                Scope: {job.remote_scope}
              </span>
            )}
          </div>
        </div>

        {/* Match Score Badge */}
        {job.match_score !== undefined && job.match_score !== null && (
          <div
            className={`flex items-center gap-1.5 px-3.5 py-2 rounded-xl border text-sm font-extrabold w-fit ${getScoreColor(
              job.match_score
            )}`}
          >
            <Flame className="w-4 h-4 fill-current" />
            <span>{Math.round(job.match_score)}% Match</span>
          </div>
        )}
      </div>

      {/* Description Snippet */}
      <p className="text-xs text-slate-300 line-clamp-2 leading-relaxed">
        {job.description
          .replace(/<[^>]*>?/gm, ' ')
          .replace(/&amp;/g, '&')
          .replace(/&lt;/g, '<')
          .replace(/&gt;/g, '>')
          .replace(/&quot;/g, '"')
          .replace(/&#39;/g, "'")
          .replace(/&nbsp;/g, ' ')
          .replace(/\s+/g, ' ')
          .trim()}
      </p>

      {/* Action Bar */}
      <div className="pt-3 border-t border-slate-800/80 flex flex-wrap items-center justify-between gap-3 text-xs">
        <div className="flex items-center gap-2">
          {/* Status Dropdown */}
          <select
            value={status}
            onChange={(e) => handleStatusUpdate(e.target.value)}
            disabled={loading}
            className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 font-semibold focus:outline-none focus:border-brand-500 cursor-pointer"
          >
            <option value="NEW">🆕 Status: NEW</option>
            <option value="SAVED">⭐ SAVED</option>
            <option value="APPLIED">🚀 APPLIED</option>
            <option value="SCREENING">🔍 SCREENING</option>
            <option value="INTERVIEW">🎙️ INTERVIEW</option>
            <option value="OFFER">🎉 OFFER</option>
            <option value="REJECTED">❌ REJECTED</option>
          </select>
        </div>

        <a
          href={job.url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={handleApplyClick}
          className="flex items-center gap-1.5 px-4 py-2 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs shadow-md transition-colors"
        >
          <span>Apply Now</span>
          <ExternalLink className="w-3.5 h-3.5" />
        </a>
      </div>
    </div>
  );
}
