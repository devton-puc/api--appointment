from sqlalchemy.exc import IntegrityError
from app.model import SessionLocal
from app.model.appointment import Appointment
from app.model.medication import Medication
from app.schemas.appointment import AppointmentSaveSchema, ListAppointmentViewSchema, AppointmentViewSchema
from app.schemas.filter import AppointmentFilterSchema
from app.schemas.status import StatusResponseSchema
from app.usecase.medication_usecase import MedicationUseCase
from app.utils.date_utils import parse_date
from app.logs.logger import logger
from typing import List
from app.schemas.medication import MedicationSchema

class AppointmentUseCase:

    def __init__(self):
        self.medication_usecase = MedicationUseCase()

    def list_appointments(self, filter_appointment: AppointmentFilterSchema) -> ListAppointmentViewSchema | StatusResponseSchema:
        try:

            session = SessionLocal()
            query = session.query(Appointment)

            if filter_appointment.patient_id:
                query = query.filter(Appointment.patient_id == filter_appointment.patient_id)

            total = query.count()
            appointments = query.offset((filter_appointment.page - 1) * filter_appointment.per_page).limit(
                filter_appointment.per_page).all()

            if not appointments:
                return StatusResponseSchema(code=204, message="Consulta não encontrada.")

            return ListAppointmentViewSchema(total=total, page=filter_appointment.page, per_page=filter_appointment.per_page,
                                             appointments=[appointment.to_view_schema() for appointment in appointments])
        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao listar as consultas", details=f"{error}")

    def create_appointment(self, appointment_data: AppointmentSaveSchema) -> StatusResponseSchema:
        try:
            session = SessionLocal()

            new_appointment = Appointment(
                patient_id=appointment_data.patient_id,
                doctor_crm=appointment_data.doctor_crm,
                date_time=parse_date(appointment_data.date_time),
                symptoms=appointment_data.symptoms
            )

            session.add(new_appointment)
            session.flush() 

            medications = self.medication_usecase.generate_medications(appointment_data.symptoms)

            if isinstance(medications, StatusResponseSchema):
                return medications

            for medication in medications:
                new_medication = Medication(
                    appointment_id=new_appointment.id,
                    name=medication.name,
                    dosage=medication.dosage,
                    instructions=medication.instructions
                )
                session.add(new_medication)

            session.commit()
            return StatusResponseSchema[List[MedicationSchema]](code=201, message="Consulta criada com sucesso.",result=medications)
        except IntegrityError:
            return StatusResponseSchema(code=500, message="Erro ao criar a consulta", details="Dados informados já existem.")
        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao criar a consulta - usecase", details=f"{error}")
 
    def update_appointment(self, id: int, appointment_data: AppointmentSaveSchema) -> StatusResponseSchema:
        try:
            session = SessionLocal()
            appointment = session.query(Appointment).get(id)
            if not appointment:
                return StatusResponseSchema(code=404, message="Consulta não encontrada.")

            if appointment_data.patient_id:
                appointment.patient_id = appointment_data.patient_id
            if appointment_data.doctor_crm:
                appointment.doctor_crm = appointment_data.doctor_crm
            if appointment_data.date_time:
                appointment.date_time = parse_date(appointment_data.date_time)
            if appointment_data.symptoms:
                appointment.symptoms = appointment_data.symptoms

                medications = self.medication_usecase.generate_medications(appointment_data.symptoms)
                if isinstance(medications, StatusResponseSchema):
                    return medications

                session.query(Medication).filter(Medication.appointment_id == id).delete()

                for medication in medications:
                    new_medication = Medication(
                        appointment_id=appointment.id,
                        name=medication.name,
                        dosage=medication.dosage,
                        instructions=medication.instructions                   )
                    session.add(new_medication)

            session.commit()
            return StatusResponseSchema[List[MedicationSchema]](code=200, message="Consulta alterada com sucesso.",result=medications)
        except IntegrityError:
            return StatusResponseSchema(code=500, message="Erro ao alterar a consulta", details="Dados já existentes.")
        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao alterar a consulta", details=f"{error}")


    def delete_appointment(self, id: int) -> StatusResponseSchema:
        try:

            session = SessionLocal()
            appointment = session.query(Appointment).get(id)
            if not appointment:
                return StatusResponseSchema(code=404, message="Consulta não encontrada.")

            session.query(Medication).filter(Medication.appointment_id == id).delete()

            session.delete(appointment)
            session.commit()
            return StatusResponseSchema(code=200, message="Consulta excluída com sucesso.")
        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao excluir a consulta", details=f"{error}")

    def get_appointment(self, id: int) -> AppointmentViewSchema | StatusResponseSchema:
        try:

            session = SessionLocal()
            appointment = session.get(Appointment, id)
            if not appointment:
                return StatusResponseSchema(code=404, message="Consulta não encontrada.")

            return AppointmentViewSchema(**appointment.to_view_schema())
        except Exception as error:
            return StatusResponseSchema(code=500, message="Erro ao obter a consulta", details=f"{error}")