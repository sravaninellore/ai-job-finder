import pytest
from app.services.collectors import (
    greenhouse_collector,
    lever_collector,
    ashby_collector,
    remoteok_collector,
    weworkremotely_collector,
    naukri_collector,
    linkedin_collector,
    wellfound_collector,
    foundit_collector,
    indeed_collector,
    glassdoor_collector,
    instahyre_collector,
    internshala_collector,
)

def test_all_13_collector_source_names():
    assert greenhouse_collector.source_name == "greenhouse"
    assert lever_collector.source_name == "lever"
    assert ashby_collector.source_name == "ashby"
    assert remoteok_collector.source_name == "remoteok"
    assert weworkremotely_collector.source_name == "weworkremotely"
    assert naukri_collector.source_name == "naukri"
    assert linkedin_collector.source_name == "linkedin"
    assert wellfound_collector.source_name == "wellfound"
    assert foundit_collector.source_name == "foundit"
    assert indeed_collector.source_name == "indeed"
    assert glassdoor_collector.source_name == "glassdoor"
    assert instahyre_collector.source_name == "instahyre"
    assert internshala_collector.source_name == "internshala"
