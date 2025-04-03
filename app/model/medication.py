from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.model import Base

class Medication(Base):
    __tablename__ = 'medication'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(Integer, ForeignKey('appointment.id'), nullable=False)
    name = Column(String(200), nullable=False)  
    dosage = Column(String(400), nullable=True) 
    instructions = Column(Text, nullable=True) 
    appointment = relationship(
        "Appointment",
        back_populates="medications"
    )

    def __init__(self, appointment_id, name, dosage=None, instructions=None):
        self.appointment_id = appointment_id
        self.name = name
        self.dosage = dosage
        self.instructions = instructions

    def to_view_schema(self):
        return {
            "id": self.id,
            "appointment_id": self.appointment_id,
            "name": self.name,
            "dosage": self.dosage,
            "instructions": self.instructions
        }
