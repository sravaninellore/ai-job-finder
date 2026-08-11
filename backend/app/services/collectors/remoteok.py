import logging
import httpx
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

class RemoteOKCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "remoteok"

    def fetch_jobs(self, target_tags: List[str] = None) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {"User-Agent": "AI-Job-Finder/1.0"}
        url = "https://remoteok.com/api"

        try:
            with httpx.Client(timeout=10.0, headers=headers) as client:
                res = client.get(url)
                if res.status_code != 200:
                    logger.warning(f"Failed to fetch RemoteOK jobs: HTTP {res.status_code}")
                    return []
                data = res.json()
                # First element is legal notice dict, actual jobs start from index 1
                items = data[1:] if isinstance(data, list) and len(data) > 1 else []

                for item in items:
                    if not isinstance(item, dict):
                        continue

                    title = item.get("position", "Software Engineer")
                    company = item.get("company", "Remote Company")
                    source_id = str(item.get("id", ""))
                    job_url = item.get("url", f"https://remoteok.com/remote-jobs/{source_id}")
                    location_name = item.get("location", "Worldwide Remote")
                    description = item.get("description", "")
                    tags = item.get("tags", [])

                    classification = location_classifier.classify(location_name, description)
                    content_hash = Job.generate_content_hash(company=company, title=title, description=description)

                    parsed_job = {
                        "source": self.source_name,
                        "source_job_id": source_id,
                        "company": company,
                        "title": title,
                        "description": description or f"{title} position at {company}",
                        "location": location_name or "Remote",
                        "country": classification["country"],
                        "city": classification["city"],
                        "work_mode": "REMOTE",
                        "remote_scope": classification["remote_scope"],
                        "employment_type": "Full-time",
                        "skills": tags,
                        "url": job_url,
                        "raw_data": item,
                        "content_hash": content_hash
                    }
                    jobs_collected.append(parsed_job)

        except Exception as e:
            logger.error(f"Error executing RemoteOK collector: {e}")

        return jobs_collected

remoteok_collector = RemoteOKCollector()
