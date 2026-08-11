import logging
import re
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

class LinkedInCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "linkedin"

    def fetch_jobs(self, keywords: List[str] = ["Software Engineer", "Full Stack Developer"], locations: List[str] = ["India", "Remote"]) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
        }

        for kw in keywords[:2]:
            for loc in locations[:2]:
                url = f"https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={kw.replace(' ', '%20')}&location={loc.replace(' ', '%20')}&start=0"
                try:
                    with httpx.Client(timeout=10.0, headers=headers) as client:
                        res = client.get(url)
                        if res.status_code != 200:
                            logger.warning(f"LinkedIn public API returned HTTP {res.status_code}")
                            continue

                        html = res.text
                        # Regex extraction of job cards from LinkedIn guest HTML
                        titles = re.findall(r'<h3 class="base-search-card__title">\s*(.*?)\s*</h3>', html, re.DOTALL)
                        companies = re.findall(r'<h4 class="base-search-card__subtitle">\s*<a[^>]*>\s*(.*?)\s*</a>', html, re.DOTALL)
                        if not companies:
                            companies = re.findall(r'<h4 class="base-search-card__subtitle">\s*(.*?)\s*</h4>', html, re.DOTALL)
                        
                        locations_extracted = re.findall(r'<span class="job-search-card__location">\s*(.*?)\s*</span>', html, re.DOTALL)
                        links = re.findall(r'<a class="base-card__full-link[^"]*" href="([^"]+)"', html)

                        count = min(len(titles), len(links))
                        for i in range(count):
                            title_clean = re.sub(r'<[^>]+>', '', titles[i]).strip()
                            comp_clean = re.sub(r'<[^>]+>', '', companies[i]).strip() if i < len(companies) else "Tech Company"
                            loc_clean = re.sub(r'<[^>]+>', '', locations_extracted[i]).strip() if i < len(locations_extracted) else loc
                            job_url = links[i].split("?")[0]
                            source_id = job_url.split("-")[-1] if "-" in job_url else str(i)

                            classification = location_classifier.classify(loc_clean, title_clean)
                            content_hash = Job.generate_content_hash(company=comp_clean, title=title_clean, description=f"{title_clean} at {comp_clean}")

                            parsed_job = {
                                "source": self.source_name,
                                "source_job_id": source_id,
                                "company": comp_clean,
                                "title": title_clean,
                                "description": f"{title_clean} position at {comp_clean} in {loc_clean}. Apply via LinkedIn.",
                                "location": loc_clean,
                                "country": classification["country"],
                                "city": classification["city"],
                                "work_mode": classification["work_mode"],
                                "remote_scope": classification["remote_scope"],
                                "employment_type": "Full-time",
                                "url": job_url,
                                "raw_data": {"title": title_clean, "company": comp_clean, "url": job_url},
                                "content_hash": content_hash
                            }
                            jobs_collected.append(parsed_job)

                except Exception as e:
                    logger.error(f"Error executing LinkedIn collector for {kw} in {loc}: {e}")

        return jobs_collected

linkedin_collector = LinkedInCollector()
