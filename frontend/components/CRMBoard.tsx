'use client';

import React, { useState, useEffect } from 'react';
import { getCRMBoard, updateJobStatus } from '@/lib/api';
import { ExternalLink, Flame, MapPin, RefreshCw, BookmarkCheck, Search, Filter } from 'lucide-react';

const COLUMNS = [
  { id: 'NEW', title: '🆕 New Jobs', color: 'border-slate-700 bg-slate-900/50' },
  { id: 'SAVED', title: '⭐ Saved', color: 'border-indigo-500/30 bg-indigo-500/5' },
  { id: 'APPLIED', title: '🚀 Applied', color: 'border-blue-500/30 bg-blue-500/5' },
  { id: 'SCREENING', title: '🔍 Screening', color: 'border-purple-500/30 bg-purple-500/5' },
  { id: 'INTERVIEW', title: '🎙️ Interview', color: 'border-amber-500/30 bg-amber-500/5' },
  { id: 'OFFER', title: '🎉 Offer', color: 'border-emerald-500/30 bg-emerald-500/5' },
  { id: 'REJECTED', title: '❌ Rejected', color: 'border-red-500/30 bg-red-500/5' },
];

export default function CRMBoard() {
  const [board, setBoard] = useState<Record<string, any[]>>({});
  const [loading, setLoading] = useState(true);

  // Search & Filters
  const [searchQuery, setSearchQuery] = useState('');
  const [minScoreFilter, setMinScoreFilter] = useState<number>(0);

  const fetchBoard = async () => {
    setLoading(true);
    try {
      const data = await getCRMBoard();
      setBoard(data);
    } catch (err) {
      console.error('Error fetching CRM board:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchBoard();
  }, []);

  const handleMoveStatus = async (jobId: string, currentStatus: string, newStatus: string) => {
    if (currentStatus === newStatus) return;

    // Optimistic UI update
    setBoard((prevBoard) => {
      const nextBoard = { ...prevBoard };
      const currentList = nextBoard[currentStatus] || [];
      const targetItem = currentList.find((item) => item.job_id === jobId);

      if (targetItem) {
        nextBoard[currentStatus] = currentList.filter((item) => item.job_id !== jobId);
        nextBoard[newStatus] = [targetItem, ...(nextBoard[newStatus] || [])];
      }
      return nextBoard;
    });

    try {
      await updateJobStatus(jobId, newStatus);
      await fetchBoard();
    } catch (err) {
      console.error('Error updating status:', err);
      fetchBoard();
    }
  };

  const filterItems = (items: any[]) => {
    return items.filter((item) => {
      const matchesQuery =
        !searchQuery ||
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.company.toLowerCase().includes(searchQuery.toLowerCase());
      const matchesScore = !minScoreFilter || (item.match_score || 0) >= minScoreFilter;
      return matchesQuery && matchesScore;
    });
  };

  if (loading) {
    return (
      <div className="p-12 text-center text-slate-400 text-sm animate-pulse">
        Loading Candidate Job Search CRM Pipeline...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Top Header & Search Bar */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <BookmarkCheck className="w-5 h-5 text-indigo-400" />
            Candidate Application CRM Pipeline
          </h2>
          <p className="text-xs text-slate-400">
            Track and move opportunities through pipeline stages: New ➔ Saved ➔ Applied ➔ Screening ➔ Interview ➔ Offer
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          {/* Search Box */}
          <div className="relative flex-1 sm:w-64">
            <Search className="w-4 h-4 absolute left-3 top-3 text-slate-500" />
            <input
              type="text"
              placeholder="Search company or role..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-2 rounded-xl bg-slate-850 border border-slate-750 text-white text-xs focus:outline-none focus:border-brand-500"
            />
          </div>

          {/* Min Score Filter */}
          <div className="flex items-center gap-1 bg-slate-850 border border-slate-750 rounded-xl px-3 py-2 text-xs">
            <Filter className="w-3.5 h-3.5 text-slate-400" />
            <select
              value={minScoreFilter}
              onChange={(e) => setMinScoreFilter(Number(e.target.value))}
              className="bg-transparent text-slate-300 font-semibold focus:outline-none cursor-pointer"
            >
              <option value={0}>All Scores</option>
              <option value={70}>≥ 70% Match</option>
              <option value={80}>≥ 80% Match</option>
            </select>
          </div>

          <button
            onClick={fetchBoard}
            className="p-2.5 rounded-xl bg-slate-800 hover:bg-slate-750 text-slate-300 text-xs flex items-center gap-1.5 transition-colors border border-slate-700 font-semibold"
          >
            <RefreshCw className="w-3.5 h-3.5" /> Refresh Board
          </button>
        </div>
      </div>

      {/* Columns Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-7 gap-4 overflow-x-auto pb-4">
        {COLUMNS.map((col) => {
          const rawItems = board[col.id] || [];
          const filteredItems = filterItems(rawItems);

          return (
            <div
              key={col.id}
              className={`p-4 rounded-2xl border ${col.color} min-h-[480px] flex flex-col space-y-3 shadow-lg`}
            >
              <div className="flex items-center justify-between pb-2 border-b border-slate-800">
                <span className="text-xs font-bold text-white">{col.title}</span>
                <span className="px-2.5 py-0.5 rounded-full bg-slate-800 text-[11px] font-extrabold text-slate-300 border border-slate-700">
                  {filteredItems.length}
                </span>
              </div>

              <div className="space-y-3 flex-grow overflow-y-auto max-h-[600px] pr-1">
                {filteredItems.length === 0 ? (
                  <p className="text-[11px] text-slate-500 italic text-center py-10">No jobs in {col.id}</p>
                ) : (
                  filteredItems.map((item) => (
                    <div
                      key={item.job_id}
                      className="p-3.5 rounded-xl bg-slate-850 border border-slate-800 hover:border-slate-700 transition-all space-y-2.5 text-xs shadow-md group"
                    >
                      <div className="space-y-0.5">
                        <span className="text-[10px] font-semibold text-brand-400 uppercase tracking-wide">
                          {item.company}
                        </span>
                        <h4 className="font-bold text-white line-clamp-1 group-hover:text-brand-300 transition-colors">
                          {item.title}
                        </h4>
                      </div>

                      <div className="flex items-center justify-between text-[11px] text-slate-400">
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3 text-indigo-400" />
                          {item.work_mode}
                        </span>
                        {item.match_score && (
                          <span className="flex items-center gap-0.5 text-amber-400 font-extrabold">
                            <Flame className="w-3 h-3 fill-current" />
                            {Math.round(item.match_score)}%
                          </span>
                        )}
                      </div>

                      <div className="pt-2 border-t border-slate-800/80 flex items-center justify-between gap-1">
                        <select
                          value={col.id}
                          onChange={(e) => handleMoveStatus(item.job_id, col.id, e.target.value)}
                          className="text-[10px] py-1 px-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-200 font-medium focus:outline-none cursor-pointer"
                        >
                          {COLUMNS.map((c) => (
                            <option key={c.id} value={c.id}>
                              Move to: {c.id}
                            </option>
                          ))}
                        </select>
                        <a
                          href={item.url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-750 text-slate-400 hover:text-white transition-colors"
                        >
                          <ExternalLink className="w-3.5 h-3.5" />
                        </a>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
