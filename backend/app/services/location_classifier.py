import re
from typing import Tuple, Dict, Any

class LocationClassifierService:
    INDIAN_CITIES = {
        "bangalore", "bengaluru", "hyderabad", "pune", "chennai",
        "mumbai", "delhi", "noida", "gurgaon", "gurugram", "kolkata", "ahmedabad", "kochi", "trivandrum"
    }

    US_KEYWORDS = {"us", "usa", "united states", "america", "us only", "pst", "est", "cst", "mst"}
    EU_KEYWORDS = {"eu", "europe", "uk", "united kingdom", "germany", "france", "netherlands", "spain", "poland"}

    @classmethod
    def classify(cls, location_text: str, description_text: str = "") -> Dict[str, Any]:
        combined = f"{location_text or ''} {description_text or ''}".lower()
        loc_lower = (location_text or "").lower()

        # 1. Determine Work Mode
        work_mode = "UNKNOWN"
        if "remote" in loc_lower or "anywhere" in loc_lower or "work from home" in loc_lower:
            work_mode = "REMOTE"
        elif "hybrid" in loc_lower:
            work_mode = "HYBRID"
        elif any(city in loc_lower for city in cls.INDIAN_CITIES) or "on-site" in loc_lower or "onsite" in loc_lower or "office" in loc_lower:
            work_mode = "ONSITE"
        elif "remote" in combined:
            work_mode = "REMOTE"

        # 2. Determine Remote Scope & Location Details
        remote_scope = "UNKNOWN"
        country = "UNKNOWN"
        city = "UNKNOWN"

        # Extract Indian cities
        found_cities = [c.title() for c in cls.INDIAN_CITIES if c in loc_lower or c in combined]
        if found_cities:
            city = found_cities[0]
            if city == "Bengaluru":
                city = "Bangalore"

        if "india" in combined or any(c in combined for c in cls.INDIAN_CITIES):
            country = "India"

        if work_mode == "REMOTE":
            if "india" in loc_lower or ("remote" in loc_lower and "india" in combined):
                remote_scope = "INDIA"
            elif "worldwide" in loc_lower or "anywhere in the world" in loc_lower or "global remote" in loc_lower:
                remote_scope = "WORLDWIDE"
            elif "us only" in loc_lower or "us remote" in loc_lower or "united states" in loc_lower:
                remote_scope = "US_ONLY"
            elif "europe" in loc_lower or "eu only" in loc_lower:
                remote_scope = "EU_ONLY"
            elif country == "India":
                remote_scope = "INDIA"
            else:
                # Default for unconstrained remote
                remote_scope = "WORLDWIDE" if not any(k in loc_lower for k in cls.US_KEYWORDS | cls.EU_KEYWORDS) else "REGION_RESTRICTED"

        elif work_mode in ("HYBRID", "ONSITE"):
            if country == "India" or city != "UNKNOWN":
                remote_scope = "INDIA"

        confidence = 0.95 if work_mode != "UNKNOWN" else 0.50

        return {
            "work_mode": work_mode,
            "remote_scope": remote_scope,
            "country": country if country != "UNKNOWN" else ("India" if "india" in combined else "Other"),
            "city": city if city != "UNKNOWN" else ("Remote" if work_mode == "REMOTE" else "Flexible"),
            "confidence": confidence,
            "evidence_text": location_text
        }

location_classifier = LocationClassifierService()
