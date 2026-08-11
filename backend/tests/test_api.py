import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base
from app.db.session import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_upload_resume_docx():
    from docx import Document
    import io

    doc = Document()
    doc.add_paragraph("Alex Johnson - Senior Developer - 4 years experience with Python, FastAPI, Docker")
    docx_io = io.BytesIO()
    doc.save(docx_io)
    docx_io.seek(0)

    files = {
        "file": ("test_resume.docx", docx_io.getvalue(), "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
    }

    response = client.post("/api/v1/resume/upload", files=files)
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["filename"] == "test_resume.docx"
    assert data["candidate_profile"]["years_of_experience"] > 0
