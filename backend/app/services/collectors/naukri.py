import logging
import re
import httpx
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

DEFAULT_ROLES = ["Software Engineer", "Full Stack Developer", "Python Developer", "React Developer", "Data Analyst"]
DEFAULT_LOCATIONS = ["Bangalore", "Hyderabad", "Pune", "Chennai", "Remote"]

class NaukriCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "naukri"

    def fetch_jobs(self, roles: List[str] = DEFAULT_ROLES, locations: List[str] = DEFAULT_LOCATIONS) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        }

        for role in roles[:2]:
            for loc in locations[:2]:
                url = f"https://www.naukri.com/{role.lower().replace(' ', '-')}-jobs-in-{loc.lower().replace(' ', '-')}"
                try:
                    with httpx.Client(timeout=10.0, headers=headers, follow_redirects=True) as client:
                        res = client.get(url)
                        if res.status_code != 200:
                            logger.warning(f"Naukri page returned HTTP {res.status_code} for {role} in {loc}")
                            continue

                        html = res.text
                        titles = re.findall(r'title="([^"]*Developer[^"]*|[^"]*Engineer[^"]*|[^"]*Analyst[^"]*)"', html, re.IGNORECASE)
                        links = re.findall(r'href="(https://www\.naukri\.com/job-listings-[^"]+)"', html)
                        companies = re.findall(r'class="subTitle fk-normal[^"]*"[^>]*>(.*?)</a>', html)

                        count = min(len(titles), len(links))
                        for i in range(count):
                            title_clean = titles[i].strip()
                            comp_clean = companies[i].strip() if i < len(companies) else "India Employer"
                            job_url = links[i]
                            source_id = job_url.split("-")[-1]

                            location_str = f"{loc}, India"
                            classification = location_classifier.classify(location_str, title_clean)
                            content_hash = Job.generate_content_hash(company=comp_clean, title=title_clean, description=f"{title_clean} position at {comp_clean}")

                            parsed_job = {
                                "source": self.source_name,
                                "source_job_id": source_id,
                                "company": comp_clean,
                                "title": title_clean,
                                "description": f"{title_clean} position at {comp_clean} in {location_str}. Apply via Naukri India.",
                                "location": location_str,
                                "country": "India",
                                "city": loc,
                                "work_mode": classification["work_mode"] if classification["work_mode"] != "UNKNOWN" else "ONSITE",
                                "remote_scope": "INDIA",
                                "employment_type": "Full-time",
                                "url": job_url,
                                "raw_data": {"title": title_clean, "company": comp_clean, "url": job_url},
                                "content_hash": content_hash
                            }
                            jobs_collected.append(parsed_job)

                except Exception as e:
                    logger.error(f"Error executing Naukri collector for {role} in {loc}: {e}")

        return jobs_collected

naukri_collector = NaukriCollector()
