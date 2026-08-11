'use client';

import React, { useEffect, useState } from 'react';
import ResumeUploader from '@/components/ResumeUploader';
import ProfileCard from '@/components/ProfileCard';
import { CandidateProfile, getLatestProfile } from '@/lib/api';
import { Sparkles, FileCheck, RefreshCw, AlertTriangle } from 'lucide-react';

export default function UploadPage() {
  const [profile, setProfile] = useState<CandidateProfile | null>(null);
  const [loadingProfile, setLoadingProfile] = useState(true);

  useEffect(() => {
    async function loadActiveProfile() {
      try {
        const result = await getLatestProfile();
        if (result && result.profile_data) {
          setProfile(result.profile_data);
        }
      } catch (err) {
        console.error('Error fetching latest profile:', err);
      } finally {
        setLoadingProfile(false);
      }
    }
    loadActiveProfile();
  }, []);

  const handleUploadSuccess = (newProfile: CandidateProfile) => {
    setProfile(newProfile);
  };

  return (
    <div className="space-y-10">
      {/* Header */}
      <div className="space-y-2 border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-brand-400 text-xs font-semibold uppercase tracking-wider">
          <Sparkles className="w-4 h-4" />
          <span>Resume & Candidate Profile Engine</span>
        </div>
        <h1 className="text-3xl font-bold text-white">Resume Parsing & Candidate Profile</h1>
        <p className="text-sm text-slate-400">
          Upload your resume (PDF or DOCX). AI will extract skills, experience, programming languages, and preferences into your candidate profile schema.
        </p>
      </div>

      {/* Upload Box */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-semibold text-slate-200 flex items-center gap-2">
            <FileCheck className="w-4 h-4 text-indigo-400" />
            {profile ? 'Upload New Version or Different Resume' : 'Upload Resume Document'}
          </h2>
          {profile && (
            <button
              onClick={() => setProfile(null)}
              className="text-xs text-slate-400 hover:text-white flex items-center gap-1 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" /> Reset View
            </button>
          )}
        </div>
        <ResumeUploader onUploadSuccess={handleUploadSuccess} />
      </div>

      {/* Render Extracted Profile */}
      {loadingProfile ? (
        <div className="p-8 text-center text-slate-400 text-sm animate-pulse">
          Checking for active candidate profile...
        </div>
      ) : profile ? (
        <div className="space-y-4 pt-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <span>Structured Candidate Profile</span>
              <span className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                Verified Facts Only
              </span>
            </h2>
          </div>
          <ProfileCard profile={profile} />
        </div>
      ) : (
        <div className="p-8 rounded-2xl bg-slate-850/40 border border-slate-800/80 text-center space-y-3">
          <AlertTriangle className="w-8 h-8 text-amber-400 mx-auto" />
          <p className="text-sm text-slate-300 font-medium">No candidate profile created yet</p>
          <p className="text-xs text-slate-500">
            Upload your resume above to extract your technical skills, roles, and job preferences.
          </p>
        </div>
      )}
    </div>
  );
}
