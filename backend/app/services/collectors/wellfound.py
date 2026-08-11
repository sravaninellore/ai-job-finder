import logging
import httpx
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

class WellfoundCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "wellfound"

    def fetch_jobs(self) -> List[Dict[str, Any]]:
        # Wellfound RSS / Public Startup API feed
        jobs_collected = []
        headers = {"User-Agent": "AI-Job-Finder/1.0"}
        url = "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss"

        try:
            with httpx.Client(timeout=10.0, headers=headers) as client:
                res = client.get(url)
                if res.status_code == 200:
                    import xml.etree.ElementTree as ET
                    root = ET.fromstring(res.text)
                    channel = root.find("channel")
                    if channel:
                        for idx, item in enumerate(channel.findall("item")[:10]):
                            title_full = item.findtext("title", "Startup Engineer")
                            link = item.findtext("link", "https://wellfound.com")
                            desc = item.findtext("description", "")
                            
                            company = "Tech Startup"
                            title = title_full
                            if ":" in title_full:
                                company, title = [p.strip() for p in title_full.split(":", 1)]

                            classification = location_classifier.classify("Remote / India", desc)
                            content_hash = Job.generate_content_hash(company=company, title=title, description=desc)

                            parsed_job = {
                                "source": self.source_name,
                                "source_job_id": f"wellfound-{idx}",
                                "company": company,
                                "title": title,
                                "description": desc or f"{title} at {company}",
                                "location": "Remote / Flexible",
                                "country": classification["country"],
                                "city": classification["city"],
                                "work_mode": "REMOTE",
                                "remote_scope": "WORLDWIDE",
                                "employment_type": "Full-time",
                                "url": link,
                                "raw_data": {"guid": f"wellfound-{idx}"},
                                "content_hash": content_hash
                            }
                            jobs_collected.append(parsed_job)

        except Exception as e:
            logger.error(f"Error executing Wellfound collector: {e}")

        return jobs_collected

wellfound_collector = WellfoundCollector()
