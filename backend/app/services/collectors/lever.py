import logging
import httpx
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

class LeverCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "lever"

    def fetch_jobs(self, company_slugs: List[str]) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {"User-Agent": "AI-Job-Finder/1.0"}

        for company in company_slugs:
            url = f"https://api.lever.co/v0/postings/{company}"
            try:
                with httpx.Client(timeout=10.0, headers=headers) as client:
                    res = client.get(url)
                    if res.status_code != 200:
                        logger.warning(f"Failed to fetch Lever jobs for company '{company}': HTTP {res.status_code}")
                        continue
                    raw_jobs = res.json()

                    for item in raw_jobs:
                        title = item.get("text", "Untitled Position")
                        source_id = str(item.get("id", ""))
                        job_url = item.get("hostedUrl", f"https://jobs.lever.co/{company}/{source_id}")
                        categories = item.get("categories", {})
                        location_name = categories.get("location", "Remote")
                        description = item.get("descriptionPlain", "") or item.get("description", "")

                        classification = location_classifier.classify(location_name, description)
                        content_hash = Job.generate_content_hash(company=company.title(), title=title, description=description)

                        parsed_job = {
                            "source": self.source_name,
                            "source_job_id": source_id,
                            "company": company.title(),
                            "title": title,
                            "description": description or f"{title} position at {company.title()}",
                            "location": location_name,
                            "country": classification["country"],
                            "city": classification["city"],
                            "work_mode": classification["work_mode"],
                            "remote_scope": classification["remote_scope"],
                            "employment_type": categories.get("commitment", "Full-time"),
                            "url": job_url,
                            "raw_data": item,
                            "content_hash": content_hash
                        }
                        jobs_collected.append(parsed_job)

            except Exception as e:
                logger.error(f"Error executing Lever collector for company '{company}': {e}")

        return jobs_collected

lever_collector = LeverCollector()
