from pydantic import BaseModel


class AskRequest(BaseModel):
    query: str


class AskResponse(BaseModel):
    success: bool
    answer: str | None = None
    country: str | None = None
    year_start: int | None = None   
    year_end: int | None = None
    future_year: int | None = None
    population_start: int | None = None
    population_end: int | None = None
    growth_rate: float | None = None
    predicted_population: int | None = None
    history: list | None = None
    error: str | None = None