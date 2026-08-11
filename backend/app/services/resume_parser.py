import json
import re
import logging
from typing import Dict, Any, List
from app.config import settings
from app.schemas.candidate import CandidateProfileSchema

logger = logging.getLogger(__name__)

RESUME_PARSER_SYSTEM_PROMPT = """
You are an expert AI Resume Parser.
Analyze the provided resume text and extract candidate information into a structured JSON object matching the exact CandidateProfile JSON schema provided.

CRITICAL INSTRUCTIONS:
1. Extract ONLY facts present in the resume. Do NOT invent, assume, or fabricate any experience, skills, roles, or degrees not explicitly mentioned.
2. Return a valid JSON object matching the exact keys below:
   - "full_name": candidate full name or null
   - "email": candidate email address or null
   - "phone": candidate phone number or null
   - "target_roles": list of job titles the candidate is qualified for or targeting
   - "years_of_experience": estimated total years of work experience as a float (e.g. 4.0)
   - "current_role": most recent job title or null
   - "previous_roles": list of objects with {"title", "company", "duration", "description"}
   - "skills": general skills/technologies mentioned
   - "programming_languages": e.g. Python, TypeScript, Java, C++, SQL
   - "tools": e.g. Git, Docker, Kubernetes, Jira, VS Code
   - "frameworks": e.g. React, Next.js, FastAPI, Django, Spring Boot, Node.js
   - "databases": e.g. PostgreSQL, MongoDB, Redis, MySQL
   - "cloud_skills": e.g. AWS, GCP, Azure, Terraform
   - "industries": e.g. FinTech, Healthcare, E-commerce, SaaS
   - "education": list of objects with {"degree", "institution", "year", "field_of_study"}
   - "certifications": list of certification names
   - "locations": preferred or current candidate locations (e.g., India, Bangalore, Remote)
   - "preferred_work_modes": e.g. ["REMOTE", "HYBRID", "ONSITE"]
   - "preferred_job_types": e.g. ["Full-time"]
   - "salary_expectation": null unless explicitly stated in resume
   - "notice_period": null unless explicitly stated in resume
   - "work_authorization": null unless explicitly stated in resume
"""

class ResumeParserService:
    def parse_resume(self, text: str) -> CandidateProfileSchema:
        # Try Gemini API if key exists
        if settings.GEMINI_API_KEY:
            try:
                return self._parse_with_gemini(text)
            except Exception as e:
                logger.warning(f"Gemini API parsing failed: {e}. Falling back to OpenAI or Heuristics.")

        # Try OpenAI API if key exists
        if settings.OPENAI_API_KEY:
            try:
                return self._parse_with_openai(text)
            except Exception as e:
                logger.warning(f"OpenAI API parsing failed: {e}. Falling back to Heuristics.")

        # Fallback heuristic parser
        return self._parse_with_heuristics(text)

    def _parse_with_gemini(self, text: str) -> CandidateProfileSchema:
        from google import genai
        client = genai.Client(api_key=settings.GEMINI_API_KEY)
        prompt = f"{RESUME_PARSER_SYSTEM_PROMPT}\n\nRESUME TEXT:\n{text}\n\nRespond ONLY with valid JSON."
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config={'response_mime_type': 'application/json'}
        )
        data = json.loads(response.text)
        return CandidateProfileSchema(**data)

    def _parse_with_openai(self, text: str) -> CandidateProfileSchema:
        import openai
        client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": RESUME_PARSER_SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract profile from this resume:\n\n{text}"}
            ]
        )
        content = response.choices[0].message.content
        data = json.loads(content)
        return CandidateProfileSchema(**data)

    def _parse_with_heuristics(self, text: str) -> CandidateProfileSchema:
        """Robust pattern matching parser used as baseline fallback when no API key is provided."""
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        
        # Email & Phone regex
        email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
        phone_match = re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', text)
        
        email = email_match.group(0) if email_match else None
        phone = phone_match.group(0) if phone_match else None
        name = lines[0] if lines and len(lines[0].split()) <= 4 else "Candidate"

        # Known skills categorization lists
        prog_languages_known = {"python", "javascript", "typescript", "java", "c++", "c#", "go", "rust", "sql", "html", "css", "php", "ruby"}
        frameworks_known = {"react", "next.js", "angular", "vue", "fastapi", "django", "flask", "spring boot", "express", "node.js", "nest.js", "tailwind css", "bootstrap"}
        databases_known = {"postgresql", "postgres", "mysql", "mongodb", "sqlite", "redis", "dynamodb", "oracle"}
        tools_known = {"git", "github", "docker", "kubernetes", "jira", "postman", "vscode", "linux"}
        cloud_known = {"aws", "gcp", "google cloud", "azure", "terraform", "docker", "kubernetes"}

        lower_text = text.lower()
        
        extracted_progs = [p.capitalize() for p in prog_languages_known if re.search(r'\b' + re.escape(p) + r'\b', lower_text)]
        extracted_frameworks = [f.title() for f in frameworks_known if re.search(r'\b' + re.escape(f) + r'\b', lower_text)]
        extracted_dbs = [d.title() for d in databases_known if re.search(r'\b' + re.escape(d) + r'\b', lower_text)]
        extracted_tools = [t.title() for t in tools_known if re.search(r'\b' + re.escape(t) + r'\b', lower_text)]
        extracted_cloud = [c.upper() for c in cloud_known if re.search(r'\b' + re.escape(c) + r'\b', lower_text)]

        # Estimate years of experience from explicit text or year patterns
        yoe = 2.0
        exp_match = re.search(r'(\d+(?:\.\d+)?)\+?\s*(?:years?|yrs?)\b', text, re.IGNORECASE)
        if exp_match:
            try:
                yoe = float(exp_match.group(1))
            except Exception:
                pass
        else:
            years = re.findall(r'\b(20\d{2}|19\d{2})\b', text)
            if len(years) >= 2:
                try:
                    int_years = [int(y) for y in years]
                    span = max(int_years) - min(int_years)
                    if 0 < span < 30:
                        yoe = float(span)
                except Exception:
                    pass

        all_skills = list(set(extracted_progs + extracted_frameworks + extracted_dbs + extracted_tools + extracted_cloud))

        return CandidateProfileSchema(
            full_name=name,
            email=email,
            phone=phone,
            target_roles=["Software Engineer", "Full Stack Developer"] if "developer" in lower_text or "engineer" in lower_text else ["Candidate"],
            years_of_experience=yoe,
            current_role="Software Engineer" if "engineer" in lower_text else lines[1] if len(lines) > 1 else None,
            previous_roles=[],
            skills=all_skills,
            programming_languages=extracted_progs,
            tools=extracted_tools,
            frameworks=extracted_frameworks,
            databases=extracted_dbs,
            cloud_skills=extracted_cloud,
            industries=["Software Development", "Information Technology"],
            education=[],
            certifications=[],
            locations=["India", "Remote"],
            preferred_work_modes=["REMOTE", "HYBRID", "ONSITE"],
            preferred_job_types=["Full-time"],
            salary_expectation=None,
            notice_period=None,
            work_authorization=None
        )

resume_parser_service = ResumeParserService()
