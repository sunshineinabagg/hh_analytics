from pydantic import BaseModel


class Vacancy(BaseModel):
    id: int | str
    name: str
    city: str | None
    salary_bottom: str | None
    salary_top: str | None
    published_at: str
    employer_name: str
    key_skills: str | None
    schedule: str
    professional_role: str
    professional_role_id: int
    experience: str
