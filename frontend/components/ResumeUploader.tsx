'use client';

import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { uploadResume, CandidateProfile } from '@/lib/api';

interface ResumeUploaderProps {
  onUploadSuccess: (profile: CandidateProfile) => void;
}

export default function ResumeUploader({ onUploadSuccess }: ResumeUploaderProps) {
  const [isDragging, setIsDragging] = useState(false);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndSetFile = (selectedFile: File) => {
    setError(null);
    setSuccess(false);

    const ext = selectedFile.name.split('.').pop()?.toLowerCase();
    if (ext !== 'pdf' && ext !== 'docx') {
      setError('Invalid file format. Please upload a PDF or DOCX resume.');
      return false;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError('File size exceeds 10MB limit.');
      return false;
    }

    setFile(selectedFile);
    return true;
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const droppedFile = e.dataTransfer.files[0];
      validateAndSetFile(droppedFile);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) return;

    setLoading(true);
    setError(null);

    try {
      const result = await uploadResume(file);
      setSuccess(true);
      if (result.candidate_profile) {
        onUploadSuccess(result.candidate_profile);
      }
    } catch (err: any) {
      setError(err.message || 'An error occurred while uploading and parsing your resume.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 sm:p-10 text-center cursor-pointer transition-all duration-300 ${
          isDragging
            ? 'border-brand-500 bg-brand-500/10 scale-[1.01]'
            : file
            ? 'border-indigo-500/50 bg-slate-800/60'
            : 'border-slate-700 bg-slate-850/50 hover:border-slate-600 hover:bg-slate-800/40'
        }`}
      >
        <input
          type="file"
          ref={fileInputRef}
          onChange={handleFileChange}
          accept=".pdf,.docx"
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-4">
          <div
            className={`p-4 rounded-2xl ${
              file ? 'bg-indigo-500/20 text-indigo-400' : 'bg-slate-800 text-slate-400'
            }`}
          >
            {file ? <FileText className="w-10 h-10" /> : <UploadCloud className="w-10 h-10" />}
          </div>

          <div>
            {file ? (
              <div className="space-y-1">
                <p className="text-base font-semibold text-white">{file.name}</p>
                <p className="text-xs text-slate-400">
                  {(file.size / (1024 * 1024)).toFixed(2)} MB • {file.name.split('.').pop()?.toUpperCase()}
                </p>
              </div>
            ) : (
              <div className="space-y-2">
                <p className="text-base font-medium text-slate-200">
                  <span className="text-brand-400 font-semibold">Click to upload</span> or drag and drop
                </p>
                <p className="text-xs text-slate-400">Supports PDF and DOCX files up to 10MB</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {error && (
        <div className="mt-4 p-4 rounded-xl bg-red-500/10 border border-red-500/30 flex items-center gap-3 text-red-400 text-sm">
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span>{error}</span>
        </div>
      )}

      {success && (
        <div className="mt-4 p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 flex items-center gap-3 text-emerald-400 text-sm">
          <CheckCircle2 className="w-5 h-5 flex-shrink-0" />
          <span>Resume successfully extracted and analyzed!</span>
        </div>
      )}

      <div className="mt-6 flex justify-end">
        <button
          onClick={handleUpload}
          disabled={!file || loading}
          className={`w-full sm:w-auto px-6 py-3 rounded-xl font-semibold text-sm flex items-center justify-center gap-2 transition-all shadow-lg ${
            !file || loading
              ? 'bg-slate-800 text-slate-500 cursor-not-allowed border border-slate-700'
              : 'bg-gradient-to-r from-brand-600 to-indigo-600 hover:from-brand-500 hover:to-indigo-500 text-white shadow-brand-500/20 active:scale-[0.99]'
          }`}
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Analyzing Resume with AI...</span>
            </>
          ) : (
            <>
              <UploadCloud className="w-4 h-4" />
              <span>Process Resume</span>
            </>
          )}
        </button>
      </div>
    </div>
  );
}
