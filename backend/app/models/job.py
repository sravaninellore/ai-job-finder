import uuid
import hashlib
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, Float, JSON, Index, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Job(Base):
    __tablename__ = "jobs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    source = Column(String(50), nullable=False, index=True)          # e.g. "greenhouse", "lever"
    source_job_id = Column(String(255), nullable=True, index=True)  # Source native ID
    company = Column(String(255), nullable=False, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    responsibilities = Column(Text, nullable=True)
    
    employment_type = Column(String(50), nullable=True)             # Full-time, Contract, etc.
    experience_min = Column(Integer, nullable=True)
    experience_max = Column(Integer, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    salary_currency = Column(String(10), nullable=True)
    
    location = Column(String(255), nullable=True)
    country = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    
    work_mode = Column(String(50), nullable=False, default="UNKNOWN")      # REMOTE, HYBRID, ONSITE, UNKNOWN
    remote_scope = Column(String(50), nullable=False, default="UNKNOWN")   # INDIA, WORLDWIDE, US_ONLY, EU_ONLY, REGION_RESTRICTED, UNKNOWN
    
    skills = Column(JSON, nullable=True, default=list)                     # Extracted skill keywords
    url = Column(String(512), nullable=False)
    company_url = Column(String(512), nullable=True)
    
    posted_at = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    discovered_at = Column(DateTime, default=datetime.utcnow)
    
    raw_data = Column(JSON, nullable=True)
    content_hash = Column(String(64), nullable=False, unique=True, index=True)

    # Relationships
    applications = relationship("JobApplication", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_job_source_sourceid", "source", "source_job_id"),
        Index("idx_job_company_title", "company", "title"),
    )

    @staticmethod
    def clean_html(text: str) -> str:
        """Strip HTML tags and unescape entities to produce clean readable text."""
        import html, re
        if not text:
            return ""
        text = html.unescape(text)
        clean = re.sub(r'<[^>]+>', ' ', text)
        return re.sub(r'\s+', ' ', clean).strip()

    @staticmethod
    def generate_content_hash(company: str, title: str, description: str) -> str:
        """Generate deterministic SHA256 content hash for job deduplication."""
        import html, re
        text = html.unescape(description or "")
        clean_desc = re.sub(r'<[^>]+>', ' ', text)
        clean_desc = re.sub(r'\s+', ' ', clean_desc).strip()
        raw_str = f"{company.strip().lower()}|{title.strip().lower()}|{clean_desc[:1000].lower()}"
        return hashlib.sha256(raw_str.encode("utf-8")).hexdigest()
