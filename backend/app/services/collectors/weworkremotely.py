import logging
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

FEED_URLS = [
    "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-front-end-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-back-end-programming-jobs.rss",
]

class WeWorkRemotelyCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "weworkremotely"

    def fetch_jobs(self, feed_urls: List[str] = FEED_URLS) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {"User-Agent": "AI-Job-Finder/1.0"}

        for feed_url in feed_urls:
            try:
                with httpx.Client(timeout=10.0, headers=headers) as client:
                    res = client.get(feed_url)
                    if res.status_code != 200:
                        logger.warning(f"Failed to fetch WeWorkRemotely RSS feed '{feed_url}': HTTP {res.status_code}")
                        continue
                    
                    root = ET.fromstring(res.text)
                    channel = root.find("channel")
                    if not channel:
                        continue

                    for item in channel.findall("item"):
                        title_full = item.findtext("title", "Software Engineer")
                        job_url = item.findtext("link", "https://weworkremotely.com")
                        description = item.findtext("description", "")
                        guid = item.findtext("guid", job_url)

                        # Title format is often: "Company: Title (Location)"
                        company = "WeWorkRemotely Partner"
                        title = title_full
                        location_name = "Worldwide Remote"

                        if ":" in title_full:
                            parts = title_full.split(":", 1)
                            company = parts[0].strip()
                            title = parts[1].strip()

                        classification = location_classifier.classify(location_name, description)
                        content_hash = Job.generate_content_hash(company=company, title=title, description=description)

                        parsed_job = {
                            "source": self.source_name,
                            "source_job_id": guid,
                            "company": company,
                            "title": title,
                            "description": description or f"{title} position at {company}",
                            "location": location_name,
                            "country": classification["country"],
                            "city": classification["city"],
                            "work_mode": "REMOTE",
                            "remote_scope": classification["remote_scope"],
                            "employment_type": "Full-time",
                            "url": job_url,
                            "raw_data": {"guid": guid, "title": title_full},
                            "content_hash": content_hash
                        }
                        jobs_collected.append(parsed_job)

            except Exception as e:
                logger.error(f"Error executing WeWorkRemotely collector for '{feed_url}': {e}")

        return jobs_collected

weworkremotely_collector = WeWorkRemotelyCollector()
