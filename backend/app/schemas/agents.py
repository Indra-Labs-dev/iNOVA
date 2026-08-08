from pydantic import BaseModel, Field


class ResearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    confirmed: bool = False


class ResearchSource(BaseModel):
    title: str
    link: str
    published: str = ""


class ResearchResponse(BaseModel):
    answer: str
    sources: list[ResearchSource] = []
    audit_id: str | None = None
    outcome: str
