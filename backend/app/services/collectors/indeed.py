import logging
import re
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

INDEED_FEEDS = [
    "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
    "https://weworkremotely.com/categories/remote-devops-sysadmin-jobs.rss"
]

class IndeedCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "indeed"

    def fetch_jobs(self, feed_urls: List[str] = INDEED_FEEDS) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        for feed_url in feed_urls:
            try:
                with httpx.Client(timeout=10.0, headers=headers, follow_redirects=True) as client:
                    res = client.get(feed_url)
                    if res.status_code != 200:
                        logger.warning(f"Indeed RSS feed returned HTTP {res.status_code} for '{feed_url}'")
                        continue

                    root = ET.fromstring(res.text)
                    channel = root.find("channel")
                    if not channel:
                        continue

                    for idx, item in enumerate(channel.findall("item")[:10]):
                        title_full = item.findtext("title", "Software Engineer")
                        job_url = item.findtext("link", "https://in.indeed.com")
                        description = item.findtext("description", "")
                        guid = item.findtext("guid", job_url)
                        company = "Indeed Tech Employer"

                        if ":" in title_full:
                            company, title_full = [p.strip() for p in title_full.split(":", 1)]

                        classification = location_classifier.classify("India", description)
                        content_hash = Job.generate_content_hash(company=company, title=title_full, description=description)

                        parsed_job = {
                            "source": self.source_name,
                            "source_job_id": f"indeed-{guid}",
                            "company": company,
                            "title": title_full,
                            "description": description or f"{title_full} position at {company}",
                            "location": "India",
                            "country": "India",
                            "city": classification["city"],
                            "work_mode": classification["work_mode"] if classification["work_mode"] != "UNKNOWN" else "ONSITE",
                            "remote_scope": classification["remote_scope"] if classification["remote_scope"] != "UNKNOWN" else "INDIA",
                            "employment_type": "Full-time",
                            "url": job_url,
                            "raw_data": {"guid": guid, "title": title_full},
                            "content_hash": content_hash
                        }
                        jobs_collected.append(parsed_job)

            except Exception as e:
                logger.error(f"Error executing Indeed collector for '{feed_url}': {e}")

        return jobs_collected

indeed_collector = IndeedCollector()
