from typing import Optional

from pydantic import BaseModel, ConfigDict

class SymptomsSchema(BaseModel):
    """
    Define os Dados para gerar as medicacoes
    """
    symptoms: str
    model_config = ConfigDict(from_attributes=True)