from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Text
from app.model import Base

class Appointment(Base):
    __tablename__ = 'appointment'

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, nullable=False)
    doctor_crm = Column(String(20), nullable=False)
    date_time = Column(DateTime, nullable=False)
    symptoms = Column(Text, nullable=False)
    medications = relationship("Medication", back_populates="appointment", cascade="all, delete-orphan")

    def __init__(self, patient_id, doctor_crm, date_time, symptoms):
        self.patient_id = patient_id
        self.doctor_crm = doctor_crm
        self.date_time = date_time
        self.symptoms = symptoms

    def to_view_schema(self):
        return {
            "id": self.id,
            "patient_id": self.patient_id,
            "doctor_crm": self.doctor_crm,
            "date_time": self.date_time.isoformat(),
            "symptoms": self.symptoms,
            "medications": [medication.to_view_schema() for medication in self.medications]
        }