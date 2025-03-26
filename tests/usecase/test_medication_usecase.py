import pytest
from app.usecase.medication_usecase import MedicationUseCase

class TestMedicationUseCase:

    @pytest.fixture
    def medication_usecase(self):
        return MedicationUseCase()

    def test_generate_medications_known_symptoms(self, medication_usecase):
        symptoms = "dor de cabeça"
        result = medication_usecase.generate_medications(symptoms)
        assert result == [
            {"name": "Paracetamol", "dosage": "500mg", "instructions": "Tomar 1 comprimido a cada 6 horas"},
            {"name": "Ibuprofeno", "dosage": "200mg", "instructions": "Tomar 1 comprimido após as refeições"},
            {"name": "Dipirona", "dosage": "1g", "instructions": "Tomar 1 cápsula somente em caso de dor"}
        ]

    def test_generate_medications_unknown_symptoms(self, medication_usecase):
        symptoms = "sintomas desconhecidos"
        result = medication_usecase.generate_medications(symptoms)
        assert result == [
            {"name": "Consultar especialista", "dosage": None, "instructions": "Nenhuma recomendação disponível"}
        ]

    def test_generate_medications_empty_input(self, medication_usecase):
        symptoms = ""
        result = medication_usecase.generate_medications(symptoms)
        assert result == [
            {"name": "Consultar especialista", "dosage": None, "instructions": "Nenhuma recomendação disponível"}
        ]