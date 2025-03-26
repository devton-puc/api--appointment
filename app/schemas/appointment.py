from pydantic import BaseModel, ConfigDict
from typing import List, Optional

from app.schemas.medication import MedicationSchema

class AppointmentSaveSchema(BaseModel):
    patient_id: int
    doctor_crm: str
    date_time: str
    symptoms: str
    medications: Optional[List[MedicationSchema]] = []

    model_config = ConfigDict(from_attributes=True)

class AppointmentViewSchema(BaseModel):
    id: int
    patient_id: int
    doctor_crm: str
    date_time: str
    symptoms: str
    medications: List[MedicationSchema]

    model_config = ConfigDict(from_attributes=True)

class ListAppointmentViewSchema(BaseModel):
    per_page: int
    page: int
    total: int
    appointments: Optional[List[AppointmentViewSchema]] = None
    model_config = ConfigDict(from_attributes=True)



class IdAppointmentPathSchema(BaseModel):
    id_appointment: int
    model_config = ConfigDict(from_attributes=True)
