import logging
import re
import httpx
from typing import List, Dict, Any
from app.services.collectors.base import BaseJobSource
from app.services.location_classifier import location_classifier
from app.models.job import Job

logger = logging.getLogger(__name__)

class InternshalaCollector(BaseJobSource):
    @property
    def source_name(self) -> str:
        return "internshala"

    def fetch_jobs(self, categories: List[str] = ["computer-science-jobs", "web-development-jobs", "python-django-jobs"]) -> List[Dict[str, Any]]:
        jobs_collected = []
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

        for category in categories:
            url = f"https://internshala.com/jobs/{category}/"
            try:
                with httpx.Client(timeout=10.0, headers=headers) as client:
                    res = client.get(url)
                    if res.status_code != 200:
                        logger.warning(f"Internshala returned HTTP {res.status_code} for category '{category}'")
                        continue

                    html = res.text
                    titles = re.findall(r'<h3 class="heading_4_5 profile"[^>]*>\s*<a[^>]*>(.*?)</a>', html, re.DOTALL)
                    companies = re.findall(r'<div class="heading_6 company_name"[^>]*>\s*<a[^>]*>(.*?)</a>', html, re.DOTALL)
                    if not companies:
                        companies = re.findall(r'<div class="heading_6 company_name"[^>]*>(.*?)</div>', html, re.DOTALL)

                    links = re.findall(r'href="(/job/detail/[^"]+)"', html)

                    count = min(len(titles), len(links))
                    for i in range(count):
                        title_clean = re.sub(r'<[^>]+>', '', titles[i]).strip()
                        comp_clean = re.sub(r'<[^>]+>', '', companies[i]).strip() if i < len(companies) else "India Developer Employer"
                        job_url = f"https://internshala.com{links[i]}"
                        source_id = links[i].split("/")[-1]

                        location_str = "India / Remote"
                        classification = location_classifier.classify(location_str, title_clean)
                        content_hash = Job.generate_content_hash(company=comp_clean, title=title_clean, description=f"{title_clean} position at {comp_clean}")

                        parsed_job = {
                            "source": self.source_name,
                            "source_job_id": source_id,
                            "company": comp_clean,
                            "title": title_clean,
                            "description": f"{title_clean} position at {comp_clean}. Apply via Internshala.",
                            "location": location_str,
                            "country": "India",
                            "city": classification["city"],
                            "work_mode": classification["work_mode"] if classification["work_mode"] != "UNKNOWN" else "REMOTE",
                            "remote_scope": "INDIA",
                            "employment_type": "Full-time / Internship",
                            "url": job_url,
                            "raw_data": {"title": title_clean, "company": comp_clean, "url": job_url},
                            "content_hash": content_hash
                        }
                        jobs_collected.append(parsed_job)

            except Exception as e:
                logger.error(f"Error executing Internshala collector for category '{category}': {e}")

        return jobs_collected

internshala_collector = InternshalaCollector()
