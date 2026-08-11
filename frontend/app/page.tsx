import Link from 'next/link';
import { Upload, Sparkles, Database, CheckCircle2, ArrowRight, FileText, Cpu, ShieldCheck } from 'lucide-react';

export default function Home() {
  return (
    <div className="space-y-16 py-4">
      {/* Hero Section */}
      <div className="text-center space-y-6 max-w-3xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-brand-500/10 border border-brand-500/20 text-brand-400 text-xs font-semibold">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Personal AI Job Match Engine</span>
        </div>

        <h1 className="text-4xl sm:text-6xl font-extrabold tracking-tight bg-gradient-to-r from-white via-slate-100 to-indigo-200 bg-clip-text text-transparent leading-[1.15]">
          Find your next job with precision AI matching
        </h1>

        <p className="text-base sm:text-lg text-slate-400 max-w-2xl mx-auto leading-relaxed">
          Upload your resume, generate a candidate profile, aggregate jobs across 13 public portals, and match opportunities with explainable AI scoring.
        </p>

        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-4">
          <Link
            href="/jobs"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold text-sm bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white shadow-xl shadow-brand-500/20 transition-all flex items-center justify-center gap-2 group"
          >
            <Database className="w-4 h-4" />
            <span>Explore Jobs Dashboard</span>
            <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
          </Link>

          <Link
            href="/upload"
            className="w-full sm:w-auto px-8 py-3.5 rounded-xl font-semibold text-sm bg-slate-800 hover:bg-slate-750 text-slate-200 border border-slate-700 transition-all flex items-center justify-center gap-2"
          >
            <Upload className="w-4 h-4" />
            <span>Upload Resume</span>
          </Link>
        </div>
      </div>

      {/* Feature Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-6 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-4 hover:border-slate-700 transition-colors">
          <div className="p-3 w-fit rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
            <FileText className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">1. Resume Analysis</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Extracts clean text from PDF/DOCX resumes and maps your experience, languages, frameworks, and job preferences into structured candidate profile data.
          </p>
          <div className="text-xs font-semibold text-blue-400 flex items-center gap-1 pt-2">
            <CheckCircle2 className="w-3.5 h-3.5" /> Feature Ready
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-4 hover:border-slate-700 transition-colors">
          <div className="p-3 w-fit rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <Database className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">2. Job Aggregation</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Collects postings from 13 job sources (Naukri, LinkedIn, Greenhouse, Lever, Ashby, Foundit, Instahyre, Indeed, Glassdoor, etc.), normalizes them into a unified schema, and classifies India & Remote scopes.
          </p>
          <div className="text-xs font-semibold text-emerald-400 flex items-center gap-1 pt-2">
            <CheckCircle2 className="w-3.5 h-3.5" /> 13 Sources Connected
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-slate-850/60 border border-slate-800 space-y-4 hover:border-slate-700 transition-colors">
          <div className="p-3 w-fit rounded-xl bg-purple-500/10 text-purple-400 border border-purple-500/20">
            <Cpu className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-white">3. AI Matching Engine</h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            Compares job requirements against candidate profile, computes 0-100 match scores, identifies missing skills, and explains why a job matches.
          </p>
          <div className="text-xs font-semibold text-purple-400 flex items-center gap-1 pt-2">
            <CheckCircle2 className="w-3.5 h-3.5" /> Multi-Score Active
          </div>
        </div>
      </div>
    </div>
  );
}
