"""
Evidence Data Model
Defines structure for retrieved commits, pull requests, issues, and discussions.
"""
from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class EvidenceItem:
    id: str
    type: str  # "Commit", "Pull Request", "Issue", "Discussion"
    title: str
    reference_id: str  # SHA (e.g. 4af3b72) or PR/Issue # (e.g. #10321)
    author: str
    date: str
    similarity_score: float
    confidence_score: float
    summary: str
    full_content: str
    url: str
    repository: str = "fastapi/fastapi"
    tags: List[str] = field(default_factory=list)
    diff_snippet: Optional[str] = None
