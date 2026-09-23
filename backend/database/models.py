from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class AnalysisRecord:
    id: Optional[int]
    text: str
    result_json: str
    created_at: Optional[datetime] = None
