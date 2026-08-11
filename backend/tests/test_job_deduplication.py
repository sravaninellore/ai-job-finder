import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.job import Job
from app.services.job_deduplicator import job_deduplicator

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_dedup.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_job_deduplication_by_hash_and_source():
    db = TestingSessionLocal()

    hash1 = Job.generate_content_hash("Stripe", "Backend Engineer", "Building global payments API.")

    job1 = Job(
        source="greenhouse",
        source_job_id="101",
        company="Stripe",
        title="Backend Engineer",
        description="Building global payments API.",
        url="https://boards.greenhouse.io/stripe/jobs/101",
        content_hash=hash1
    )
    db.add(job1)
    db.commit()

    # Test exact duplicate by source_job_id
    assert job_deduplicator.is_duplicate(db, "greenhouse", "101", "https://boards.greenhouse.io/stripe/jobs/101", hash1) == True

    # Test duplicate by content hash with different source_job_id
    assert job_deduplicator.is_duplicate(db, "lever", "999", "https://jobs.lever.co/stripe/999", hash1) == True

    # Test new unique job
    hash2 = Job.generate_content_hash("Stripe", "Frontend Engineer", "Building React Dashboard.")
    assert job_deduplicator.is_duplicate(db, "greenhouse", "102", "https://boards.greenhouse.io/stripe/jobs/102", hash2) == False
    
    db.close()
