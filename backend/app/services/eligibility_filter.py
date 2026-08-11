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

        # 1. Work Mode & Location Check
        if job.work_mode not in preference.allowed_work_modes and job.work_mode != "UNKNOWN":
            eligible = False
            reasons.append(f"Work mode '{job.work_mode}' is not in allowed preferences ({', '.join(preference.allowed_work_modes)}).")

        # 2. Remote Scope Check
        if job.work_mode == "REMOTE":
            if job.remote_scope in ("US_ONLY", "EU_ONLY", "REGION_RESTRICTED"):
                if "WORLDWIDE" not in preference.allowed_remote_scopes and job.remote_scope not in preference.allowed_remote_scopes:
                    eligible = False
                    reasons.append(f"Remote scope is restricted to '{job.remote_scope}', which does not cover India/Worldwide preference.")
            elif job.remote_scope not in preference.allowed_remote_scopes and job.remote_scope != "UNKNOWN":
                warnings.append(f"Remote scope is '{job.remote_scope}'. Please verify regional eligibility.")

        # 3. Onsite / Hybrid City Check
        if job.work_mode in ("ONSITE", "HYBRID"):
            job_city = (job.city or "").strip().lower()
            allowed_cities = [c.lower() for c in preference.preferred_cities]
            if job_city and job_city not in ("unknown", "remote", "flexible"):
                if not any(city in job_city for city in allowed_cities) and "India" not in job.country:
                    eligible = False
                    reasons.append(f"On-site location '{job.city}' is outside preferred cities ({', '.join(preference.preferred_cities)}).")

        # 4. Experience Requirement Bounds Check
        cand_yoe = candidate.years_of_experience or 0.0
        if job.experience_min is not None:
            if job.experience_min > cand_yoe + preference.max_experience_tolerance:
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
