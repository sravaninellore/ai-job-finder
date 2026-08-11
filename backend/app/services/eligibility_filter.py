from typing import Dict, Any, List
from app.models.job import Job
from app.schemas.candidate import CandidateProfileSchema
from app.schemas.preference import CandidatePreferenceSchema
from app.schemas.eligibility import EligibilityResult

class JobEligibilityFilterService:
    @staticmethod
    def evaluate(job: Job, candidate: CandidateProfileSchema, preference: CandidatePreferenceSchema) -> EligibilityResult:
        reasons: List[str] = []
        warnings: List[str] = []
        eligible = True

        # 1. Work Mode & Location Check (Only enforce if preferences specified)
        if preference.allowed_work_modes and job.work_mode not in preference.allowed_work_modes and job.work_mode != "UNKNOWN":
            eligible = False
            reasons.append(f"Work mode '{job.work_mode}' is not in allowed preferences ({', '.join(preference.allowed_work_modes)}).")

        # 2. Remote Scope Check
        if job.work_mode == "REMOTE":
            j_scope = (job.remote_scope or "UNKNOWN").upper()
            if j_scope in ("US_ONLY", "EU_ONLY", "REGION_RESTRICTED"):
                has_worldwide = any("WORLDWIDE" in s.upper() for s in (preference.allowed_remote_scopes or []))
                if not has_worldwide and not any(j_scope in s.upper() for s in (preference.allowed_remote_scopes or [])):
                    eligible = False
                    reasons.append(f"Remote scope is restricted to '{job.remote_scope}', which does not cover candidate preferences.")
            elif preference.allowed_remote_scopes and j_scope != "UNKNOWN":
                matches = False
                for s in preference.allowed_remote_scopes:
                    s_upper = s.upper()
                    if ("INDIA" in s_upper and "INDIA" in j_scope) or ("WORLDWIDE" in s_upper and "WORLDWIDE" in j_scope) or (s_upper in j_scope or j_scope in s_upper):
                        matches = True
                        break
                if not matches:
                    eligible = False
                    reasons.append(f"Remote scope '{job.remote_scope}' does not match allowed scopes ({', '.join(preference.allowed_remote_scopes)}).")

        # 3. Onsite / Hybrid City Check
        if job.work_mode in ("ONSITE", "HYBRID") and preference.preferred_cities:
            job_city = (job.city or "").strip().lower()
            allowed_cities = [c.lower() for c in preference.preferred_cities]
            if job_city and job_city not in ("unknown", "remote", "flexible"):
                if not any(city in job_city for city in allowed_cities) and "India" not in (job.country or ""):
                    eligible = False
                    reasons.append(f"On-site location '{job.city}' is outside preferred cities ({', '.join(preference.preferred_cities)}).")

        # 4. Experience Requirement Bounds Check
        cand_yoe = candidate.years_of_experience or 0.0
        if job.experience_min is not None:
            if job.experience_min > cand_yoe + (preference.max_experience_tolerance or 2.0):
                eligible = False
                reasons.append(f"Requires minimum {job.experience_min} years experience; candidate has {cand_yoe:.1f} years.")

        if job.experience_max is not None and job.experience_max < cand_yoe - 3.0:
            warnings.append(f"Candidate experience ({cand_yoe:.1f} yrs) exceeds job maximum ({job.experience_max} yrs). Candidate may be overqualified.")

        return EligibilityResult(
            eligible=eligible,
            reasons=reasons,
            warnings=warnings
        )

eligibility_filter = JobEligibilityFilterService()
