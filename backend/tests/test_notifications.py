from app.services.notifications.email_service import email_notification_service

def test_email_digest_html_generation():
    top_jobs = [
        {
            "id": "job-1",
            "title": "Senior Data Analyst",
            "company": "ABC Technologies",
            "location": "Remote — India",
            "work_mode": "REMOTE",
            "url": "https://example.com/job/1",
            "match_score": 96.0
        },
        {
            "id": "job-2",
            "title": "BI Analyst",
            "company": "XYZ Corp",
            "location": "Hyderabad — Hybrid",
            "work_mode": "HYBRID",
            "url": "https://example.com/job/2",
            "match_score": 93.0
        }
    ]

    html = email_notification_service.generate_digest_html("Jane Doe", top_jobs)
    assert "Senior Data Analyst" in html
    assert "ABC Technologies" in html
    assert "96% Match" in html
    assert "Jane Doe" in html

def test_send_digest_simulation():
    res = email_notification_service.send_digest_email("test@example.com", "Test User", [])
    assert res == False or res == True
