const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1';

export interface CandidateProfile {
  full_name?: string;
  email?: string;
  phone?: string;
  target_roles: string[];
  years_of_experience: number;
  current_role?: string;
  previous_roles: Array<{ title: string; company?: string; duration?: string; description?: string }>;
  skills: string[];
  programming_languages: string[];
  tools: string[];
  frameworks: string[];
  databases: string[];
  cloud_skills: string[];
  industries: string[];
  education: Array<{ degree: string; institution?: string; year?: string; field_of_study?: string }>;
  certifications: string[];
  locations: string[];
  preferred_work_modes: string[];
  preferred_job_types: string[];
  salary_expectation?: string;
  notice_period?: string;
  work_authorization?: string;
}

export interface CandidateProfileResponse {
  id: string;
  resume_id: string;
  profile_data: CandidateProfile;
  created_at: string;
  updated_at: string;
}

export interface Job {
  id: string;
  source: string;
  source_job_id?: string;
  company: string;
  title: string;
  description: string;
  requirements?: string;
  responsibilities?: string;
  employment_type?: string;
  experience_min?: number;
  experience_max?: number;
  salary_min?: number;
  salary_max?: number;
  salary_currency?: string;
  location?: string;
  country?: string;
  city?: string;
  work_mode: string;
  remote_scope: string;
  skills: string[];
  url: string;
  company_url?: string;
  posted_at?: string;
  discovered_at: string;
  content_hash: string;
  match_score?: number;
  match_recommendation?: string;
  application_status?: string;
}

export interface CandidatePreference {
  allowed_work_modes: string[];
  allowed_remote_scopes: string[];
  preferred_cities: string[];
  allowed_employment_types: string[];
  min_match_percentage: number;
  max_experience_tolerance: number;
}

export interface TrackerSummary {
  total_jobs: number;
  saved_jobs: number;
  applied_jobs: number;
  interview_jobs: number;
  offer_jobs: number;
  high_match_jobs: number;
}

export async function uploadResume(file: File): Promise<{
  id: string;
  filename: string;
  candidate_profile: CandidateProfile;
}> {
  const formData = new FormData();
  formData.append('file', file);

  const response = await fetch(`${API_BASE_URL}/resume/upload`, {
    method: 'POST',
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Upload failed' }));
    throw new Error(errorData.detail || 'Failed to upload resume');
  }

  return response.json();
}

export async function getLatestProfile(): Promise<CandidateProfileResponse | null> {
  try {
    const response = await fetch(`${API_BASE_URL}/profile/latest`, { cache: 'no-store' });
    if (response.status === 404) return null;
    if (!response.ok) throw new Error('Failed to fetch candidate profile');
    return response.json();
  } catch (err) {
    console.warn('API error fetching candidate profile:', err);
    return null;
  }
}

export async function triggerJobIngestion(): Promise<{ message: string; ingested: number }> {
  const response = await fetch(`${API_BASE_URL}/jobs/trigger-ingest`, { method: 'POST' });
  if (!response.ok) throw new Error('Failed to ingest jobs');
  return response.json();
}

export async function getJobs(params?: { work_mode?: string; remote_scope?: string; source?: string; min_score?: number }): Promise<Job[]> {
  const query = new URLSearchParams();
  if (params?.work_mode) query.set('work_mode', params.work_mode);
  if (params?.remote_scope) query.set('remote_scope', params.remote_scope);
  if (params?.source) query.set('source', params.source);
  if (params?.min_score) query.set('min_score', params.min_score.toString());

  const response = await fetch(`${API_BASE_URL}/jobs?${query.toString()}`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Failed to fetch jobs');
  return response.json();
}

export async function runMatchingAll(): Promise<{ message: string; jobs_matched: number }> {
  const response = await fetch(`${API_BASE_URL}/matching/run-all`, { method: 'POST' });
  if (!response.ok) throw new Error('Failed to run AI matching engine');
  return response.json();
}

export async function getPreferences(): Promise<CandidatePreference> {
  const response = await fetch(`${API_BASE_URL}/preferences`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Failed to fetch preferences');
  return response.json();
}

export async function updatePreferences(data: CandidatePreference): Promise<CandidatePreference> {
  const response = await fetch(`${API_BASE_URL}/preferences`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to update preferences');
  return response.json();
}

export async function updateJobStatus(jobId: string, status: string, notes?: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/tracking/job/${jobId}/status`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ status, notes }),
  });
  if (!response.ok) throw new Error('Failed to update job status');
  return response.json();
}

export async function getTrackerSummary(): Promise<TrackerSummary> {
  const response = await fetch(`${API_BASE_URL}/tracking/summary`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Failed to fetch tracker summary');
  return response.json();
}

export async function getCRMBoard(): Promise<Record<string, any[]>> {
  const response = await fetch(`${API_BASE_URL}/tracking/board`, { cache: 'no-store' });
  if (!response.ok) throw new Error('Failed to fetch CRM board');
  return response.json();
}

export async function sendTestEmail(recipientEmail: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/alerts/test-email`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipient_email: recipientEmail }),
  });
  if (!response.ok) throw new Error('Failed to send test email');
  return response.json();
}

export async function triggerDailyDigest(recipientEmail: string): Promise<any> {
  const response = await fetch(`${API_BASE_URL}/alerts/trigger-daily-digest`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ recipient_email: recipientEmail }),
  });
  if (!response.ok) throw new Error('Failed to trigger daily digest email');
  return response.json();
}
