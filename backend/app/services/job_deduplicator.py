import logging
from sqlalchemy.orm import Session
from app.models.job import Job

logger = logging.getLogger(__name__)

class JobDeduplicatorService:
    @staticmethod
    def is_duplicate(db: Session, source: str, source_job_id: str, url: str, content_hash: str) -> bool:
        """Check if job is duplicate using:
           1. source + source_job_id
           2. normalized URL
           3. content_hash
        """
        # 1. Check source + source_job_id
        if source_job_id:
            existing = db.query(Job).filter(Job.source == source, Job.source_job_id == source_job_id).first()
            if existing:
                logger.info(f"Duplicate found by source ({source}) and source_job_id ({source_job_id})")
                return True

        # 2. Check URL
        normalized_url = url.strip().rstrip('/')
        existing_url = db.query(Job).filter(Job.url.like(f"{normalized_url}%")).first()
        if existing_url:
            logger.info(f"Duplicate found by normalized URL ({normalized_url})")
            return True

        # 3. Check content_hash
        existing_hash = db.query(Job).filter(Job.content_hash == content_hash).first()
        if existing_hash:
            logger.info(f"Duplicate found by SHA256 content_hash ({content_hash})")
            return True

        return False

job_deduplicator = JobDeduplicatorService()
