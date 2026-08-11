from app.services.resume_parser import ResumeParserService

def test_heuristic_resume_parser():
    resume_text = """
    Jane Smith
    email: jane.smith@example.com
    phone: +1-555-123-4567

    Professional Summary:
    Senior Software Engineer with 5 years of experience building modern web applications.

    Technical Skills:
    Programming Languages: Python, TypeScript, SQL
    Frameworks: FastAPI, React, Next.js, Django
    Databases: PostgreSQL, Redis
    Tools: Git, Docker, Kubernetes
    Cloud: AWS, GCP
    """

    parser = ResumeParserService()
    profile = parser._parse_with_heuristics(resume_text)

    assert profile.email == "jane.smith@example.com"
    assert "Python" in profile.programming_languages
    assert "Fastapi" in profile.frameworks or "FastAPI" in [f.title() for f in profile.frameworks]
    assert "Postgresql" in profile.databases or "Postgres" in profile.databases
    assert "Docker" in profile.tools
    assert profile.years_of_experience >= 1.0
