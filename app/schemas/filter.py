from typing import Optional

from pydantic import BaseModel, ConfigDict


class AppointmentFilterSchema(BaseModel):
    """
    Define os Dados para filtrar a consulta do paciente
    """
    per_page: int
    page: int
    symptoms: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
