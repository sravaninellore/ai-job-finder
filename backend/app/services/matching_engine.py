import json
import logging
from typing import Dict, Any
from app.config import settings
from app.models.job import Job
from app.schemas.candidate import CandidateProfileSchema
from app.schemas.match import MatchAnalysisResult

logger = logging.getLogger(__name__)

MATCHING_SYSTEM_PROMPT = """
You are an expert AI Talent Evaluator.
Compare the Candidate Profile against the Job Posting and produce a multi-dimensional match score JSON.

SCORING FORMULA & WEIGHTS:
1. skill_score (0-100): Overlap and semantic alignment between candidate technical skills/languages/frameworks and job requirements.
2. experience_score (0-100): Alignment of years of experience and level of seniority.
3. role_score (0-100): Relevance of candidate target/current/previous roles to job title & responsibilities.
4. location_score (0-100): Work mode (Remote/Hybrid/Onsite) and location compatibility.
5. education_score (0-100): Degree and field of study alignment.

CRITICAL INSTRUCTIONS:
- Do NOT invent candidate experience or pretend candidate has skills not listed in the candidate profile.
- Highlight missing required skills in "missing_skills".
- Overall score MUST be calculated as:
  overall_score = (skill_score * 0.30) + (experience_score * 0.25) + (role_score * 0.20) + (location_score * 0.20) + (education_score * 0.05)
- Recommendation must be one of: "highly_recommended" (>=85), "recommended" (70-84), "possible" (50-69), "poor" (<50).
- Return valid JSON matching the exact structure.
"""

class MatchingEngineService:
    def match(self, candidate: CandidateProfileSchema, job: Job) -> MatchAnalysisResult:
        # Try Gemini API if key is present
        if settings.GEMINI_API_KEY:
            try:
                return self._match_with_gemini(candidate, job)
            except Exception as e:
                logger.warning(f"Gemini AI matching failed: {e}. Falling back to Rule Matcher.")

        # Try OpenAI API if key is present
        if settings.OPENAI_API_KEY:
            try:
                return self._match_with_openai(candidate, job)
            except Exception as e:
                logger.warning(f"OpenAI AI matching failed: {e}. Falling back to Rule Matcher.")

        # Heuristic Deterministic Match Engine
        return self._match_with_heuristics(candidate, job)

    def _match_with_gemini(self, candidate: CandidateProfileSchema, job: Job) -> MatchAnalysisResult:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        payload = {
            "candidate": candidate.model_dump(),
            "job": {
                "title": job.title,
                "company": job.company,
                "description": job.description[:2000],
                "location": job.location,
                "work_mode": job.work_mode,
                "remote_scope": job.remote_scope,
                "experience_min": job.experience_min,
                "experience_max": job.experience_max
            }
        }
        prompt = f"{MATCHING_SYSTEM_PROMPT}\n\nEVALUATION INPUT:\n{json.dumps(payload)}\n\nRespond ONLY with valid JSON."
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        data = json.loads(response.text)
        return MatchAnalysisResult(**data)

    def _match_with_openai(self, candidate: CandidateProfileSchema, job: Job) -> MatchAnalysisResult:
        import openai
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        payload = {
            "candidate": candidate.model_dump(),
            "job": {
                "title": job.title,
                "company": job.company,
                "description": job.description[:2000],
                "location": job.location,
                "work_mode": job.work_mode,
                "remote_scope": job.remote_scope
            }
        }
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": MATCHING_SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(payload)}
            ]
        )
        data = json.loads(response.choices[0].message.content)
        return MatchAnalysisResult(**data)

    def _match_with_heuristics(self, candidate: CandidateProfileSchema, job: Job) -> MatchAnalysisResult:
        cand_skills = set([s.lower() for s in (candidate.skills + candidate.programming_languages + candidate.frameworks + candidate.tools + candidate.databases + candidate.cloud_skills)])
        job_text = (f"{job.title} {job.description} {job.requirements or ''}").lower()

        # Skill Overlap
        matched_skills = [s for s in cand_skills if s in job_text]
        skill_score = min(100.0, (len(matched_skills) / max(1, len(cand_skills))) * 150.0) if cand_skills else 60.0

        # Experience Overlap
        cand_yoe = candidate.years_of_experience or 0.0
        min_req = job.experience_min or 0
        exp_diff = abs(cand_yoe - min_req)
        exp_score = max(30.0, 100.0 - (exp_diff * 12.0))

        # Role score
        role_score = 75.0
        if any(r.lower() in job.title.lower() for r in (candidate.target_roles or [])):
            role_score = 95.0

        # Location score
        location_score = 90.0 if job.work_mode in ("REMOTE", "HYBRID") else 70.0

        # Weighted calculation
        overall = (skill_score * 0.30) + (exp_score * 0.25) + (role_score * 0.20) + (location_score * 0.20) + (80.0 * 0.05)

        recommendation = "highly_recommended" if overall >= 85 else "recommended" if overall >= 70 else "possible" if overall >= 50 else "poor"

        return MatchAnalysisResult(
            overall_score=round(overall, 1),
            skill_score=round(skill_score, 1),
            experience_score=round(exp_score, 1),
            role_score=round(role_score, 1),
            location_score=round(location_score, 1),
            education_score=80.0,
            strengths=[f"Matched skills: {', '.join(matched_skills[:5])}"] if matched_skills else ["Solid experience alignment"],
            missing_skills=[],
            concerns=[] if overall >= 70 else ["Experience bounds mismatch"],
            recommendation=recommendation,
            explanation=f"Evaluated match score of {overall:.1f}% based on technical skills and work mode compatibility."
        )

matching_engine = MatchingEngineService()
