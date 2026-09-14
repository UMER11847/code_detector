from pydantic import BaseModel, Field
from typing import List


class Finding(BaseModel):
    severity: str = Field(
        description="Severity level: Critical, High, Medium, or Low"
    )
    category: str = Field(
        description="Category such as Bug, Security, Performance, or Code Quality"
    )
    title: str
    description: str
    suggestion: str


class CodeReview(BaseModel):
    summary: str
    findings: List[Finding]
    improved_code: str
