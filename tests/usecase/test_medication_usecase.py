import pytest
from unittest.mock import patch, MagicMock
from app.schemas.status import StatusResponseSchema
from app.schemas.medication import MedicationSchema
from app.usecase.medication_usecase import MedicationUseCase
from app.usecase import GEMINI_AI_URL, OPENAI_TOKEN

class TestMedicationUseCase:

    @pytest.fixture
    def mock_response(self):
        return {
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "```json\n[\n  {\n    \"name\": \"Omeprazol\",\n    \"dosage\": \"20mg\",\n    \"instructions\": \"Tomar 1 cápsula em jejum pela manhã.\"\n  },\n  {\n    \"name\": \"Ibuprofeno\",\n    \"dosage\": \"400mg\",\n    \"instructions\": \"Tomar 1 comprimido a cada 6-8 horas, conforme necessário.\"\n  },\n  {\n    \"name\": \"Dimenidrinato\",\n    \"dosage\": \"50mg\",\n    \"instructions\": \"Tomar 1 comprimido 30 minutos antes das refeições ou viagens.\"\n  }\n]\n```"
                            }
                        ]
                    }
                }
            ]
        }

    @pytest.fixture
    def mock_response_error(self):
        return {                
            "candidates": [
                {
                    "content": {
                        "parts": [
                            {
                                "text": "Isso não é um JSON válido!"                                
                            }
                        ]
                    }
                }
            ]
        }


    @pytest.fixture
    def medication_usecase(self):
        return MedicationUseCase()

    @patch('app.usecase.medication_usecase.requests.post')
    def test_should_generate_medications_when_success(self, mock_post, medication_usecase, mock_response):

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response
       
        symptoms = "dor no estomago, garganta inflamada, nauseas"
        
        medications = medication_usecase.generate_medications(symptoms)

        assert isinstance(medications, list) 
        assert all(isinstance(med, MedicationSchema) for med in medications) 
        assert len(medications) == 3  
        assert medications[0].name == "Omeprazol"  
        assert medications[1].dosage == "400mg" 
        assert medications[2].instructions == "Tomar 1 comprimido 30 minutos antes das refeições ou viagens." 

    @patch('app.usecase.medication_usecase.requests.post')
    def test_should_generate_medications_when_error(self, mock_post, medication_usecase):

        mock_post.side_effect = Exception("Erro ao simular medicações.")
        
        symptoms = "dor no estomago, garganta inflamada, nauseas"        
        response = medication_usecase.generate_medications(symptoms)
        
        assert isinstance(response, StatusResponseSchema)  
        assert response.code == 500  
        assert "Erro ao simular medicações." in response.message 


    @patch('app.usecase.medication_usecase.requests.post')
    def test_should_generate_medications_when_json_invalid(self, mock_post, medication_usecase, mock_response_error):

        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = mock_response_error

        symptoms = "dor no estomago, garganta inflamada, nauseas"

        response = medication_usecase.generate_medications(symptoms)
        assert isinstance(response, StatusResponseSchema)  
