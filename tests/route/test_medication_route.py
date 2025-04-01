import pytest
from app import app
from unittest.mock import MagicMock
from unittest.mock import patch
from app.schemas.filter import AppointmentFilterSchema
from app.schemas.status import StatusResponseSchema
from app.schemas.medication import MedicationSchema
from app.usecase.medication_usecase import MedicationUseCase

from tests.mock.medication_mock import (
    mock_generate_medications_success,
    mock_generate_medications_failure_400,
    mock_generate_medications_failure_500
)

@pytest.fixture
def client():
    """Mocka a sessão do banco e retorna um cliente de teste do Flask"""
    with patch("app.model.SessionLocal", MagicMock()):
        app.testing = True
        with app.test_client() as client:
            yield client

class TestMedicationRoute:

    def test_should_return_http200_generate_medications_when_success(self, client):
        with patch("app.usecase.medication_usecase.MedicationUseCase.generate_medications", mock_generate_medications_success()):
            sysmptoms_data = {
                "symptoms": "febre"
            }
            response = client.post("/appointment/medications/generate", json=sysmptoms_data)
            assert response.status_code == 200

    def test_should_return_http400_generate_medications_when_success(self, client):
        with patch("app.usecase.medication_usecase.MedicationUseCase.generate_medications", mock_generate_medications_failure_400()):
            sysmptoms_data = {
                "symptoms": "febre"
            }
            response = client.post("/appointment/medications/generate", json=sysmptoms_data)
            assert response.status_code == 400


    def test_should_return_http500_generate_medications_when_success(self, client):
        with patch("app.usecase.medication_usecase.MedicationUseCase.generate_medications", mock_generate_medications_failure_500()):
            sysmptoms_data = {
                "symptoms": "febre"
            }
            response = client.post("/appointment/medications/generate", json=sysmptoms_data)
            assert response.status_code == 500            
 