import pytest
from unittest.mock import MagicMock, patch
from app.usecase.appointment_usecase import AppointmentUseCase
from app.schemas.status import StatusResponseSchema
from app.schemas.appointment import AppointmentViewSchema, ListAppointmentViewSchema, AppointmentSaveSchema
from app.model.appointment import Appointment
from app.model.medication import Medication
from app.schemas.filter import AppointmentFilterSchema
from app.schemas.medication import MedicationSchema
from sqlalchemy.exc import IntegrityError

class TestAppointmentUseCase:


    @pytest.fixture
    def setup_usecase(self):
        return AppointmentUseCase()

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_list_appointments_when_success(self, session_mock, setup_usecase):
 
        filter_appointment = AppointmentFilterSchema(page=1, per_page=5, patient_id=1)

        mock_medication_1 = MagicMock(spec=Medication)
        mock_medication_1.to_view_schema.return_value = {
            "id": 1,
            "appointment_id": 10,
            "name": "Paracetamol",
            "dosage": "500mg",
            "instructions": "Tomar a cada 6 horas"
        }

        mock_medication_2 = MagicMock(spec=Medication)
        mock_medication_2.to_view_schema.return_value = {
            "id": 2,
            "appointment_id": 11,
            "name": "Ibuprofeno",
            "dosage": "200mg",
            "instructions": "Tomar após as refeições"
        }

        mock_appointment = MagicMock(spec=Appointment)
        mock_appointment.id = 10
        mock_appointment.patient_id = 1
        mock_appointment.doctor_crm = "123456"
        mock_appointment.date_time = "2025-03-30T00:00:00"
        mock_appointment.symptoms = "dor de cabeça"
        mock_appointment.medications = [mock_medication_1, mock_medication_2]
        mock_appointment.to_view_schema.return_value = {
            "id": mock_appointment.id,
            "patient_id": mock_appointment.patient_id,
            "doctor_crm": mock_appointment.doctor_crm,
            "date_time": mock_appointment.date_time,
            "symptoms": mock_appointment.symptoms,
            "medications": [medication.to_view_schema() for medication in mock_appointment.medications]
        }

        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query  
        mock_query.count.return_value = 1  
        mock_query.offset.return_value.limit.return_value.all.return_value = [mock_appointment]

        mock_session = session_mock.return_value
        mock_session.query.return_value = mock_query

        response = setup_usecase.list_appointments(filter_appointment)

        assert isinstance(response, ListAppointmentViewSchema)
        assert response.total == 1
        assert response.page == filter_appointment.page
        assert response.per_page == filter_appointment.per_page
        assert len(response.appointments) == 1
        assert response.appointments[0].id == mock_appointment.id
        assert len(response.appointments[0].medications) == 2

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_list_appointments_when_no_results(self, session_mock, setup_usecase):

        filter_appointment = AppointmentFilterSchema(page=1, per_page=5, patient_id=1)

        mock_session = session_mock.return_value
        mock_session.query.return_value.filter.return_value.offset.return_value.limit.return_value.all.return_value = []
        mock_session.query.return_value.count.return_value = 0

        response = setup_usecase.list_appointments(filter_appointment)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 204
        assert response.message == "Consulta não encontrada."

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_list_appointments_when_error(self, session_mock, setup_usecase):

        filter_appointment = AppointmentFilterSchema(page=1, per_page=5, patient_id=1)

        mock_session = session_mock.return_value
        mock_session.query.side_effect = Exception("Erro inesperado no banco de dados")

        response = setup_usecase.list_appointments(filter_appointment)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao listar as consultas"
        assert "Erro inesperado no banco de dados" in response.details

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_create_appointment_when_success(self, session_mock, setup_usecase):

        mock_medications = [
            MedicationSchema(name="Paracetamol", dosage="500mg", instructions="Tomar a cada 6 horas"),
            MedicationSchema(name="Ibuprofeno", dosage="200mg", instructions="Tomar após as refeições")
        ]

        appointment_data = AppointmentSaveSchema(
            patient_id=1,
            doctor_crm="123456",
            date_time="2025-03-30T00:00:00",
            symptoms="dor de cabeça",
            medications=mock_medications
        )

        mock_session = session_mock.return_value
        mock_session.add.return_value = None
        mock_session.flush.return_value = None
        mock_session.commit.return_value = None

        response = setup_usecase.create_appointment(appointment_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 201
        assert response.message == "Consulta criada com sucesso."

        assert mock_session.add.call_count == 3  


    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_create_appointment_when_integrity_error(self, session_mock, setup_usecase):

        mock_medications = [
            MedicationSchema(name="Paracetamol", dosage="500mg", instructions="Tomar a cada 6 horas"),
            MedicationSchema(name="Ibuprofeno", dosage="200mg", instructions="Tomar após as refeições")
        ]

        appointment_data = AppointmentSaveSchema(
            patient_id=1,
            doctor_crm="123456",
            date_time="2025-03-30T00:00:00",
            symptoms="dor de cabeça",
            medications = mock_medications
        )



        mock_session = session_mock.return_value
        mock_session.add.return_value = None
        mock_session.flush.return_value = None
        mock_session.commit.side_effect = IntegrityError("Integrity error", None, None)

        response = setup_usecase.create_appointment(appointment_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao criar a consulta"
        assert response.details == "Dados informados já existem."


    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_create_appointment_when_error(self, session_mock, setup_usecase):

        mock_medications = [
            MedicationSchema(name="Paracetamol", dosage="500mg", instructions="Tomar a cada 6 horas"),
            MedicationSchema(name="Ibuprofeno", dosage="200mg", instructions="Tomar após as refeições")
        ]

        appointment_data = AppointmentSaveSchema(
            patient_id=1,
            doctor_crm="123456",
            date_time="2025-03-30T00:00:00",
            symptoms="dor de cabeça",
            medications=mock_medications
        )

        mock_session = session_mock.return_value
        mock_session.add.return_value = None
        mock_session.flush.return_value = None
        mock_session.commit.side_effect = Exception("Erro inesperado")

        response = setup_usecase.create_appointment(appointment_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao criar a consulta - usecase"
        assert "Erro inesperado" in response.details

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_update_appointment_when_success(self, session_mock, setup_usecase):

        mock_medications = [
            MedicationSchema(name="Paracetamol", dosage="500mg", instructions="Tomar a cada 6 horas"),
            MedicationSchema(name="Ibuprofeno", dosage="200mg", instructions="Tomar após as refeições")
        ]

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-03-30T00:00:00",
            symptoms="febre",
            medications = mock_medications
        )

        mock_appointment = MagicMock(spec=Appointment)
        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_appointment
        mock_session.query.return_value.filter.return_value.delete.return_value = None
        mock_session.commit.return_value = None

        response = setup_usecase.update_appointment(1, appointment_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 200
        assert response.message == "Consulta alterada com sucesso."

        assert mock_session.query.return_value.filter.return_value.delete.called
        assert mock_session.add.call_count == 2  # Apenas medicações adicionadas

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_update_appointment_when_not_found(self, session_mock, setup_usecase):

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-03-30T00:00:00",
            symptoms="febre"
        )

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = None

        response = setup_usecase.update_appointment(1, appointment_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 404
        assert response.message == "Consulta não encontrada."

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_update_appointment_when_integrity_error(self, session_mock, setup_usecase):


        mock_medications = [
            MedicationSchema(name="Paracetamol", dosage="500mg", instructions="Tomar a cada 6 horas"),
            MedicationSchema(name="Ibuprofeno", dosage="200mg", instructions="Tomar após as refeições")
        ]

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-03-30T00:00:00",
            symptoms="febre",
            medications=mock_medications
        )

        mock_appointment = MagicMock(spec=Appointment)
        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_appointment
        mock_session.query.return_value.filter.return_value.delete.return_value = None
        mock_session.commit.side_effect = IntegrityError("Integrity error", None, None)

        response = setup_usecase.update_appointment(1, appointment_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao alterar a consulta"
        assert response.details == "Dados já existentes."

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_update_appointment_when_error(self, session_mock, setup_usecase):

        mock_medications = [
            MedicationSchema(name="Paracetamol", dosage="500mg", instructions="Tomar a cada 6 horas"),
            MedicationSchema(name="Ibuprofeno", dosage="200mg", instructions="Tomar após as refeições")
        ]

        appointment_data = AppointmentSaveSchema(
            patient_id=2,
            doctor_crm="654321",
            date_time="2025-03-30T00:00:00",
            symptoms="febre",
            medications=mock_medications
        )


        mock_appointment = MagicMock(spec=Appointment)
        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_appointment
        mock_session.query.return_value.filter.return_value.delete.return_value = None
        mock_session.commit.side_effect = Exception("Erro inesperado")

        response = setup_usecase.update_appointment(1, appointment_data)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao alterar a consulta"
        assert "Erro inesperado" in response.details

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_delete_appointment_when_success(self, session_mock, setup_usecase):
        mock_appointment = MagicMock(spec=Appointment)
        mock_appointment.id = 1

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_appointment
        mock_session.delete.return_value = None
        mock_session.commit.return_value = None

        response = setup_usecase.delete_appointment(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 200
        assert response.message == "Consulta excluída com sucesso."

        mock_session.delete.assert_called_once_with(mock_appointment)
        mock_session.commit.assert_called_once()

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_delete_appointment_when_not_found(self, session_mock, setup_usecase):
        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = None

        response = setup_usecase.delete_appointment(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 404
        assert response.message == "Consulta não encontrada."

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_delete_appointment_when_error(self, session_mock, setup_usecase):
        mock_appointment = MagicMock(spec=Appointment)
        mock_appointment.id = 1

        mock_session = session_mock.return_value
        mock_session.query.return_value.get.return_value = mock_appointment
        mock_session.delete.side_effect = Exception("Erro ao excluir a consulta")

        response = setup_usecase.delete_appointment(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao excluir a consulta"

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_return_appointment_when_found(self, session_mock, setup_usecase):

        mock_medication = MagicMock(spec=Medication)
        mock_medication.to_view_schema.return_value = {
            "id": 2,
            "appointment_id": 1,
            "name": "Paracetamol",
            "dosage": "500mg",
            "instructions": "Tomar após as refeições"
        }

        mock_medication_2 = MagicMock(spec=Medication)
        mock_medication_2.to_view_schema.return_value = {
            "id": 1,
            "appointment_id": 1,
            "name": "Ibuprofeno",
            "dosage": "200mg",
            "instructions": "Tomar a cada 6 horas"
        }

        mock_appointment = MagicMock(spec=Appointment)
        mock_appointment.id = 1
        mock_appointment.medications = [mock_medication, mock_medication_2]
        mock_appointment.to_view_schema.return_value = {
            "id": 1,
            "patient_id": 1,
            "doctor_crm": "123456",
            "date_time": "2025-03-25T15:00:00",
            "symptoms": "dor de cabeça",
            "medications": [med.to_view_schema() for med in mock_appointment.medications]
 
        }

        mock_session = session_mock.return_value
        mock_session.get.return_value = mock_appointment

        response = setup_usecase.get_appointment(1)

        assert isinstance(response, AppointmentViewSchema)
        assert response.id == 1
        assert response.patient_id == 1
        assert response.doctor_crm == "123456"
        assert response.date_time == "2025-03-25T15:00:00"
        assert response.symptoms == "dor de cabeça"
        assert response.medications[0].name == "Paracetamol"
        assert response.medications[0].dosage == "500mg"
        assert response.medications[0].instructions == "Tomar após as refeições"
        assert response.medications[1].name == "Ibuprofeno"
        assert response.medications[1].dosage == "200mg"
        assert response.medications[1].instructions == "Tomar a cada 6 horas"


    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_return_appointment_when_not_found(self, session_mock, setup_usecase):
        mock_session = session_mock.return_value
        mock_session.get.return_value = None

        response = setup_usecase.get_appointment(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 404
        assert response.message == "Consulta não encontrada."

    @patch("app.usecase.appointment_usecase.SessionLocal")
    def test_should_return_appointment_when_error(self, session_mock, setup_usecase):
        mock_session = session_mock.return_value
        mock_session.get.side_effect = Exception("Erro ao obter a consulta")

        response = setup_usecase.get_appointment(1)

        assert isinstance(response, StatusResponseSchema)
        assert response.code == 500
        assert response.message == "Erro ao obter a consulta"