from pydantic import BaseModel
from typing import List, Optional
from pydantic import EmailStr, ConfigDict

class MedicationSchema(BaseModel):
    id: int
    appointment_id: int
    name: str
    dosage: Optional[str] = None
    instructions: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)