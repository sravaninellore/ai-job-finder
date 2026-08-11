from abc import ABC, abstractmethod
from typing import List
from app.models.job import Job

class BaseJobSource(ABC):
    @property
    @abstractmethod
    def source_name(self) -> str:
        """Name of the job source, e.g. 'greenhouse', 'lever'."""
        pass

    @abstractmethod
    def fetch_jobs(self, board_tokens: List[str]) -> List[dict]:
        """Fetch job postings from external API and convert into dictionary list matching Job schema."""
        pass
