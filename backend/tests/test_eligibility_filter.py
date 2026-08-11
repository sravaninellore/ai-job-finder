from app.models.job import Job
from app.schemas.candidate import CandidateProfileSchema
from app.schemas.preference import CandidatePreferenceSchema
from app.services.eligibility_filter import eligibility_filter

def test_eligibility_filter_valid_remote_india():
    job = Job(
        title="Software Engineer",
        company="TechCorp",
        description="Great role",
        url="https://example.com",
        work_mode="REMOTE",
        remote_scope="INDIA",
        experience_min=3,
        content_hash="dummy"
    )

    candidate = CandidateProfileSchema(years_of_experience=4.0)
    preference = CandidatePreferenceSchema(
        allowed_work_modes=["REMOTE", "HYBRID"],
        allowed_remote_scopes=["INDIA", "WORLDWIDE"]
    )

    res = eligibility_filter.evaluate(job, candidate, preference)
    assert res.eligible == True
    assert len(res.reasons) == 0

def test_eligibility_filter_reject_us_only():
    job = Job(
        title="US Engineer",
        company="USCorp",
        description="US strictly",
        url="https://example.com",
        work_mode="REMOTE",
        remote_scope="US_ONLY",
        experience_min=3,
        content_hash="dummy"
    )

    candidate = CandidateProfileSchema(years_of_experience=4.0)
    preference = CandidatePreferenceSchema(
        allowed_work_modes=["REMOTE"],
        allowed_remote_scopes=["INDIA"]
    )

    res = eligibility_filter.evaluate(job, candidate, preference)
    assert res.eligible == False
    assert any("US_ONLY" in r for r in res.reasons)
