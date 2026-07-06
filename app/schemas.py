from pydantic import BaseModel, Field


class Event(BaseModel):
    title: str = Field(description="The name or title of the tech event.")
    date: str = Field(description="The date or date range of the event.")
    location: str = Field(
        description="The location of the event (city, country, online, etc.)."
    )
    relevance_score: int = Field(
        description="Relevance score from 0 to 100 based on the target developer profile (cloud infrastructure, Go, Python, systems monitoring, AI engineering)."
    )
    justification: str = Field(
        description="Explanation/justification for the relevance score."
    )
