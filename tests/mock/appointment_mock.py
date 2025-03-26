from unittest.mock import MagicMock
from app.schemas.status import StatusResponseSchema
from app.schemas.appointment import AppointmentViewSchema, ListAppointmentViewSchema
from app.schemas.medication import MedicationSchema

def mock_list_appointments_success():
    mock = MagicMock()
    mock.return_value = ListAppointmentViewSchema(
        per_page=5,
        page=1,
        total=2,
        appointments=[
            AppointmentViewSchema(
                id=1,
                patient_id=101,
                doctor_crm="CRM12345",
                date_time="2025-04-01T12:00:00",
                symptoms="febre",
                medications=[]
            ),
            AppointmentViewSchema(
                id=2,
                patient_id=102,
                doctor_crm="CRM54321",
                date_time="2025-04-02T15:00:00",
                symptoms="dor de cabeça",
                medications=[]
            )
        ]
    )
    return mock

def mock_list_appointments_failure_204():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=204,
        details="Nenhum paciente encontrado",
        message="Nenhum paciente encontrado"
    )
    return mock

def mock_list_appointments_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno do servidor",
        message="Ocorreu um erro ao tentar listar os pacientes"
    )
    return mock

def mock_get_appointment_success():
    mock = MagicMock()
    mock.return_value = AppointmentViewSchema(
        id=1,
        patient_id=101,
        doctor_crm="CRM12345",
        date_time="02/02/2020",
        symptoms="febre",
        medications=[
            MedicationSchema(
                id=1001,
                appointment_id=1,
                name="Paracetamol",
                dosage="500mg",
                instructions="Tomar 1 comprimido a cada 8 horas"
            ),
            MedicationSchema(
                id=1002,
                appointment_id=1,
                name="Ibuprofeno",
                dosage="200mg",
                instructions="Tomar após as refeições"
            )
        ]
    )
    return mock

def mock_get_appointment_failure_404():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=404,
        details="Paciente não encontrado",
        message="Não foi possível encontrar o paciente"
    )
    return mock


def mock_get_appointment_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno do servidor",
        message="Ocorreu um erro ao tentar obter o paciente"
    )
    return mock
    
def mock_create_appointment_success():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=201,
        details=None,
        message="Consulta criado com sucesso."
    )
    return mock


def mock_create_appointment_failure_400():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=400,
        details="Erro na validação dos dados da consulta.",
        message="Erro ao validar dados da consulta."
    )
    return mock

def mock_create_appointment_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno no servidor.",
        message="Ocorreu um erro ao tentar criar a consulta."
    )
    return mock

def mock_update_appointment_success():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=200,
        details=None,
        message="Consulta alterada com sucesso."
    )
    return mock


def mock_update_appointment_failure_404():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=404,
        details="Consulta não encontrada",
        message="Não foi possível encontrar a consulta para atualizar."
    )
    return mock


def mock_update_appointment_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno no servidor.",
        message="Ocorreu um erro ao tentar atualizar a consulta."
    )
    return mock

def mock_delete_appointment_success():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=200,
        details=None,
        message="Consulta deletada com sucesso."
    )
    return mock

def mock_delete_appointment_failure_404():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=404,
        details="Consulta não encontrada",
        message="Não foi possível encontrar a consulta para excluir."
    )
    return mock

def mock_delete_appointment_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno no servidor.",
        message="Ocorreu um erro ao tentar excluir a consulta."
    )
    return mock
