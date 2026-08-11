'use client';

import React from 'react';
import { CandidateProfile } from '@/lib/api';
import SkillBadge from './SkillBadge';
import {
  User,
  Briefcase,
  Code,
  Wrench,
  Layers,
  Database,
  Cloud,
  GraduationCap,
  MapPin,
  Clock,
  DollarSign,
  ShieldCheck,
  Building,
  Award
} from 'lucide-react';

interface ProfileCardProps {
  profile: CandidateProfile;
}

export default function ProfileCard({ profile }: ProfileCardProps) {
  return (
    <div className="space-y-6">
      {/* Header Banner */}
      <div className="p-6 sm:p-8 rounded-2xl bg-gradient-to-r from-slate-850 via-slate-900 to-indigo-950/40 border border-slate-800 shadow-xl relative overflow-hidden">
        <div className="absolute -right-10 -bottom-10 w-40 h-40 bg-brand-500/10 rounded-full blur-3xl pointer-events-none"></div>

        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="space-y-1.5">
            <div className="flex items-center gap-3">
              <div className="p-2.5 rounded-xl bg-brand-500/20 text-brand-400 border border-brand-500/30">
                <User className="w-6 h-6" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-white">{profile.full_name || 'Candidate Profile'}</h1>
                <p className="text-sm font-medium text-brand-400">
                  {profile.current_role || 'Software Engineering Professional'}
                </p>
              </div>
            </div>
            {(profile.email || profile.phone) && (
              <div className="flex flex-wrap gap-4 text-xs text-slate-400 pt-2">
                {profile.email && <span>📧 {profile.email}</span>}
                {profile.phone && <span>📞 {profile.phone}</span>}
              </div>
            )}
          </div>

          <div className="flex items-center gap-3">
            <div className="px-4 py-2 rounded-xl bg-slate-800/80 border border-slate-700 text-center">
              <span className="block text-2xl font-extrabold text-indigo-400">
                {profile.years_of_experience}
              </span>
              <span className="text-[10px] uppercase tracking-wider font-semibold text-slate-400">
                Years Exp
              </span>
            </div>
          </div>
        </div>

        {/* Target Roles */}
        {profile.target_roles && profile.target_roles.length > 0 && (
          <div className="mt-6 pt-4 border-t border-slate-800/80 flex flex-wrap items-center gap-2">
            <span className="text-xs font-semibold text-slate-400 flex items-center gap-1.5 mr-2">
              <Briefcase className="w-3.5 h-3.5 text-indigo-400" /> Target Roles:
            </span>
            {profile.target_roles.map((role, idx) => (
              <span
                key={idx}
                className="px-2.5 py-1 rounded-md text-xs font-medium bg-indigo-500/15 text-indigo-300 border border-indigo-500/20"
              >
                {role}
              </span>
            ))}
          </div>
        )}
      </div>

      {/* Grid of Categorized Skills & Attributes */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Programming Languages */}
        {profile.programming_languages && profile.programming_languages.length > 0 && (
          <div className="p-5 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
              <Code className="w-4 h-4 text-blue-400" />
              <span>Programming Languages</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.programming_languages.map((lang, idx) => (
                <SkillBadge key={idx} label={lang} category="programming" />
              ))}
            </div>
          </div>
        )}

        {/* Frameworks & Libraries */}
        {profile.frameworks && profile.frameworks.length > 0 && (
          <div className="p-5 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
              <Layers className="w-4 h-4 text-indigo-400" />
              <span>Frameworks & Libraries</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.frameworks.map((fw, idx) => (
                <SkillBadge key={idx} label={fw} category="framework" />
              ))}
            </div>
          </div>
        )}

        {/* Databases */}
        {profile.databases && profile.databases.length > 0 && (
          <div className="p-5 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
              <Database className="w-4 h-4 text-emerald-400" />
              <span>Databases</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.databases.map((db, idx) => (
                <SkillBadge key={idx} label={db} category="database" />
              ))}
            </div>
          </div>
        )}

        {/* Cloud & DevOps */}
        {profile.cloud_skills && profile.cloud_skills.length > 0 && (
          <div className="p-5 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
              <Cloud className="w-4 h-4 text-amber-400" />
              <span>Cloud & Infrastructure</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.cloud_skills.map((cloud, idx) => (
                <SkillBadge key={idx} label={cloud} category="cloud" />
              ))}
            </div>
          </div>
        )}

        {/* Tools & Environment */}
        {profile.tools && profile.tools.length > 0 && (
          <div className="p-5 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
              <Wrench className="w-4 h-4 text-purple-400" />
              <span>Tools & Platforms</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.tools.map((tool, idx) => (
                <SkillBadge key={idx} label={tool} category="tool" />
              ))}
            </div>
          </div>
        )}

        {/* All / Other General Skills */}
        {profile.skills && profile.skills.length > 0 && (
          <div className="p-5 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-3">
            <div className="flex items-center gap-2 text-sm font-semibold text-slate-200">
              <Award className="w-4 h-4 text-pink-400" />
              <span>Extracted Core Skills</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {profile.skills.map((skill, idx) => (
                <SkillBadge key={idx} label={skill} category="default" />
              ))}
            </div>
          </div>
        )}
      </div>

      {/* Preferences & Metadata */}
      <div className="p-6 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-4">
        <h3 className="text-sm font-semibold text-slate-300 uppercase tracking-wider">
          Job Preferences & Context
        </h3>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 text-xs">
          <div className="flex items-center gap-2 text-slate-300">
            <MapPin className="w-4 h-4 text-indigo-400 flex-shrink-0" />
            <span>
              Locations:{' '}
              <strong className="text-white">
                {profile.locations && profile.locations.length > 0 ? profile.locations.join(', ') : 'Not specified'}
              </strong>
            </span>
          </div>

          <div className="flex items-center gap-2 text-slate-300">
            <Clock className="w-4 h-4 text-brand-400 flex-shrink-0" />
            <span>
              Work Modes:{' '}
              <strong className="text-white">
                {profile.preferred_work_modes && profile.preferred_work_modes.length > 0
                  ? profile.preferred_work_modes.join(', ')
                  : 'Remote / Any'}
              </strong>
            </span>
          </div>

          <div className="flex items-center gap-2 text-slate-300">
            <Building className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>
              Job Types:{' '}
              <strong className="text-white">
                {profile.preferred_job_types && profile.preferred_job_types.length > 0
                  ? profile.preferred_job_types.join(', ')
                  : 'Full-time'}
              </strong>
            </span>
          </div>

          {profile.salary_expectation && (
            <div className="flex items-center gap-2 text-slate-300">
              <DollarSign className="w-4 h-4 text-amber-400 flex-shrink-0" />
              <span>
                Salary Exp: <strong className="text-white">{profile.salary_expectation}</strong>
              </span>
            </div>
          )}

          {profile.notice_period && (
            <div className="flex items-center gap-2 text-slate-300">
              <Clock className="w-4 h-4 text-purple-400 flex-shrink-0" />
              <span>
                Notice Period: <strong className="text-white">{profile.notice_period}</strong>
              </span>
            </div>
          )}

          {profile.work_authorization && (
            <div className="flex items-center gap-2 text-slate-300">
              <ShieldCheck className="w-4 h-4 text-blue-400 flex-shrink-0" />
              <span>
                Work Auth: <strong className="text-white">{profile.work_authorization}</strong>
              </span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
