import logging
import httpx
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

class GreenhouseCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "greenhouse"

    def fetch_jobs(self, board_tokens: List[str]) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {"User-Agent": "AI-Job-Finder/1.0"}

        for token in board_tokens:
            url = f"https://boards-api.greenhouse.io/v1/boards/{token}/jobs?content=true"
            try:
                with httpx.Client(timeout=10.0, headers=headers) as client:
                    res = client.get(url)
                    if res.status_code != 200:
                        logger.warning(f"Failed to fetch Greenhouse jobs for board '{token}': HTTP {res.status_code}")
                        continue
                    data = res.json()
                    raw_jobs = data.get("jobs", [])

                    for item in raw_jobs:
                        title = item.get("title", "Untitled Position")
                        source_id = str(item.get("id", ""))
                        company = token.title()
                        job_url = item.get("absolute_url", f"https://boards.greenhouse.io/{token}/jobs/{source_id}")
                        description = Job.clean_html(item.get("content", "")) or f"{title} position at {company}"
                        location_name = item.get("location", {}).get("name", "Remote / Flexible")

                        # Classify location & remote scope
                        classification = location_classifier.classify(location_name, description)

                        # Generate SHA256 content hash
                        content_hash = Job.generate_content_hash(company=company, title=title, description=description)

                        parsed_job = {
                            "source": self.source_name,
                            "source_job_id": source_id,
                            "company": company,
                            "title": title,
                            "description": content or f"{title} position at {token.title()}",
                            "location": location_name,
                            "country": classification["country"],
                            "city": classification["city"],
                            "work_mode": classification["work_mode"],
                            "remote_scope": classification["remote_scope"],
                            "employment_type": "Full-time",
                            "url": job_url,
                            "raw_data": item,
                            "content_hash": content_hash
                        }
                        jobs_collected.append(parsed_job)

            except Exception as e:
                logger.error(f"Error executing Greenhouse collector for board '{token}': {e}")

        return jobs_collected

greenhouse_collector = GreenhouseCollector()
