import logging
import httpx
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

class AshbyCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "ashby"

    def fetch_jobs(self, board_names: List[str]) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {"User-Agent": "AI-Job-Finder/1.0"}

        for board in board_names:
            url = f"https://api.ashbyhq.com/posting-api/job-board/{board}?includePostingType=true"
            try:
                with httpx.Client(timeout=10.0, headers=headers) as client:
                    res = client.get(url)
                    if res.status_code != 200:
                        logger.warning(f"Failed to fetch Ashby jobs for board '{board}': HTTP {res.status_code}")
                        continue
                    data = res.json()
                    jobs_list = data.get("jobs", [])

                    for item in jobs_list:
                        title = item.get("title", "Untitled Position")
                        source_id = str(item.get("id", ""))
                        job_url = item.get("jobUrl", f"https://jobs.ashbyhq.com/{board}/{source_id}")
                        location_name = item.get("locationName", "Remote")
                        description = item.get("descriptionHtml", "") or item.get("descriptionPlain", "")

                        classification = location_classifier.classify(location_name, description)
                        content_hash = Job.generate_content_hash(company=board.title(), title=title, description=description)

                        parsed_job = {
                            "source": self.source_name,
                            "source_job_id": source_id,
                            "company": board.title(),
                            "title": title,
                            "description": description or f"{title} position at {board.title()}",
                            "location": location_name,
                            "country": classification["country"],
                            "city": classification["city"],
                            "work_mode": classification["work_mode"],
                            "remote_scope": classification["remote_scope"],
                            "employment_type": item.get("employmentType", "Full-time"),
                            "url": job_url,
                            "raw_data": item,
                            "content_hash": content_hash
                        }
                        jobs_collected.append(parsed_job)

            except Exception as e:
                logger.error(f"Error executing Ashby collector for board '{board}': {e}")

        return jobs_collected

ashby_collector = AshbyCollector()
