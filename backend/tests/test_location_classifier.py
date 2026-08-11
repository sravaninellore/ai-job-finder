from app.services.location_classifier import location_classifier

def test_location_classification_india_remote():
    res = location_classifier.classify("Remote - India", "Full stack engineer position based in India")
    assert res["work_mode"] == "REMOTE"
    assert res["remote_scope"] == "INDIA"
    assert res["country"] == "India"

def test_location_classification_worldwide_remote():
    res = location_classifier.classify("Remote (Worldwide)", "Work from anywhere in the world")
    assert res["work_mode"] == "REMOTE"
    assert res["remote_scope"] == "WORLDWIDE"

def test_location_classification_us_only():
    res = location_classifier.classify("Remote (US Only)", "Must be located in United States")
    assert res["work_mode"] == "REMOTE"
    assert res["remote_scope"] == "US_ONLY"

def test_location_classification_bangalore_onsite():
    res = location_classifier.classify("Bangalore, India", "Onsite role at tech park")
    assert res["work_mode"] == "ONSITE"
    assert res["city"] == "Bangalore"
    assert res["country"] == "India"
