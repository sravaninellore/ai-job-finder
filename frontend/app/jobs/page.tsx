'use client';

import React, { useState, useEffect } from 'react';
import { Job, TrackerSummary, getJobs, triggerJobIngestion, runMatchingAll, getTrackerSummary } from '@/lib/api';
import JobCard from '@/components/JobCard';
import JobFilters from '@/components/JobFilters';
import {
  Sparkles,
  RefreshCw,
  Cpu,
  Briefcase,
  BookmarkCheck,
  Flame,
  Send,
  Loader2
} from 'lucide-react';

export default function JobsPage() {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [summary, setSummary] = useState<TrackerSummary | null>(null);
  const [loadingJobs, setLoadingJobs] = useState(true);

  const [ingesting, setIngesting] = useState(false);
  const [matching, setMatching] = useState(false);

  // Filters
  const [workMode, setWorkMode] = useState('');
  const [remoteScope, setRemoteScope] = useState('');
  const [source, setSource] = useState('');
  const [minScore, setMinScore] = useState(0);

  const loadData = async () => {
    setLoadingJobs(true);
    try {
      const [fetchedJobs, summaryData] = await Promise.all([
        getJobs({ work_mode: workMode, remote_scope: remoteScope, source: source, min_score: minScore }),
        getTrackerSummary(),
      ]);
      setJobs(fetchedJobs);
      setSummary(summaryData);
    } catch (err) {
      console.error('Error fetching jobs:', err);
    } finally {
      setLoadingJobs(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [workMode, remoteScope, source, minScore]);

  const handleIngest = async () => {
    setIngesting(true);
    try {
      await triggerJobIngestion();
      await loadData();
    } catch (err) {
      console.error('Ingestion failed:', err);
    } finally {
      setIngesting(false);
    }
  };

  const handleRunMatching = async () => {
    setMatching(true);
    try {
      await runMatchingAll();
      await loadData();
    } catch (err) {
      console.error('Matching failed:', err);
    } finally {
      setMatching(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Top Banner & Control Buttons */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div className="space-y-1">
          <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="w-4 h-4" />
            <span>13 Job Portals Connected</span>
          </div>
          <h1 className="text-3xl font-bold text-white">AI Job Search Dashboard</h1>
          <p className="text-sm text-slate-400">
            Normalized jobs collected across 13 public job platforms, filtered for location & remote scope, matched with explainable AI scores.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={handleIngest}
            disabled={ingesting}
            className="px-4 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-200 font-semibold text-xs border border-slate-700 flex items-center gap-2 shadow-sm transition-all"
          >
            {ingesting ? <Loader2 className="w-4 h-4 animate-spin" /> : <RefreshCw className="w-4 h-4" />}
            <span>Fetch New Jobs</span>
          </button>

          <button
            onClick={handleRunMatching}
            disabled={matching}
            className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white font-semibold text-xs flex items-center gap-2 shadow-lg shadow-brand-500/20 transition-all"
          >
            {matching ? <Loader2 className="w-4 h-4 animate-spin" /> : <Cpu className="w-4 h-4" />}
            <span>Run AI Matching</span>
          </button>
        </div>
      </div>

      {/* Top Metric Summary Cards */}
      {summary && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-1">
            <div className="text-xs font-semibold text-slate-400 flex items-center gap-1.5">
              <Briefcase className="w-4 h-4 text-indigo-400" /> Total Discovered
            </div>
            <p className="text-2xl font-extrabold text-white">{summary.total_jobs}</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-1">
            <div className="text-xs font-semibold text-slate-400 flex items-center gap-1.5">
              <Flame className="w-4 h-4 text-amber-400" /> Highly Matched (≥80%)
            </div>
            <p className="text-2xl font-extrabold text-amber-400">{summary.high_match_jobs}</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-1">
            <div className="text-xs font-semibold text-slate-400 flex items-center gap-1.5">
              <BookmarkCheck className="w-4 h-4 text-emerald-400" /> Saved Jobs
            </div>
            <p className="text-2xl font-extrabold text-emerald-400">{summary.saved_jobs}</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-1">
            <div className="text-xs font-semibold text-slate-400 flex items-center gap-1.5">
              <Send className="w-4 h-4 text-blue-400" /> Applied
            </div>
            <p className="text-2xl font-extrabold text-blue-400">{summary.applied_jobs}</p>
          </div>
        </div>
      )}

      {/* Filters Bar */}
      <JobFilters
        workMode={workMode}
        setWorkMode={setWorkMode}
        remoteScope={remoteScope}
        setRemoteScope={setRemoteScope}
        source={source}
        setSource={setSource}
        minScore={minScore}
        setMinScore={setMinScore}
      />

      {/* Job Cards Stream */}
      {loadingJobs ? (
        <div className="p-12 text-center text-slate-400 text-sm animate-pulse">
          Loading matching job postings...
        </div>
      ) : jobs.length === 0 ? (
        <div className="p-12 rounded-2xl bg-slate-850/40 border border-slate-800 text-center space-y-4">
          <Briefcase className="w-10 h-10 text-slate-500 mx-auto" />
          <p className="text-base font-semibold text-slate-300">No jobs found matching filters</p>
          <p className="text-xs text-slate-500 max-w-md mx-auto">
            Click "Fetch New Jobs" above to fetch postings from all active job sources.
          </p>
          <button
            onClick={handleIngest}
            className="px-6 py-2.5 rounded-xl bg-brand-600 hover:bg-brand-500 text-white font-semibold text-xs shadow-md"
          >
            Fetch Jobs Now
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {jobs.map((job) => (
            <JobCard key={job.id} job={job} onStatusChange={loadData} />
          ))}
        </div>
      )}
    </div>
  );
}
