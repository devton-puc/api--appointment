from unittest.mock import MagicMock
from app.schemas.status import StatusResponseSchema
from app.schemas.medication import MedicationSchema

def mock_generate_medications_success():
    mock = MagicMock()
    mock.return_value = [
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
    
    return mock

def mock_generate_medications_failure_400():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=400,
        details="Erro na validação dos dados.",
        message="Erro ao gerar os medicamentos.",
    )
    return mock

def mock_generate_medications_failure_500():
    mock = MagicMock()
    mock.return_value = StatusResponseSchema(
        code=500,
        details="Erro interno no servidor.",
        message="Erro ao gerar os medicamentos.",
    )
    return mock