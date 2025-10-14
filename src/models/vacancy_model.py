from pydantic import BaseModel


class Vacancy(BaseModel):
    id: int | str
    name: str
    city: str | None
    salary_bottom: int | float | str | None
    salary_top: int | float | str | None
    currency: str | None
    published_at: str
    employer_name: str
    key_skills: str | None
    schedule: str
    professional_role: str
    professional_role_id: int
    experience: str
