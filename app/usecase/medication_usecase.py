from app.schemas.status import StatusResponseSchema

class MedicationUseCase:
    def generate_medications(self, symptoms: str) -> list[MedicationSchema] | StatusResponseSchema:
        try:
            mock_medications = {
                "dor de cabeça": [
                    {"name": "Paracetamol", "dosage": "500mg", "instructions": "Tomar 1 comprimido a cada 6 horas"},
                    {"name": "Ibuprofeno", "dosage": "200mg", "instructions": "Tomar 1 comprimido após as refeições"},
                    {"name": "Dipirona", "dosage": "1g", "instructions": "Tomar 1 cápsula somente em caso de dor"}
                ],
                "febre": [
                    {"name": "Paracetamol", "dosage": "500mg", "instructions": "Tomar 1 comprimido a cada 8 horas"},
                    {"name": "Aspirina", "dosage": "500mg", "instructions": "Tomar 1 comprimido com bastante líquido"}
                ],
                "dor muscular": [
                    {"name": "Diclofenaco", "dosage": "50mg", "instructions": "Tomar 1 comprimido pela manhã e outro à noite"},
                    {"name": "Cataflam", "dosage": "50mg", "instructions": "Tomar 1 comprimido após o almoço"},
                    {"name": "Relaxante muscular", "dosage": "10mg", "instructions": "Tomar 1 comprimido antes de dormir"}
                ],
                "gripe": [
                    {"name": "Antigripal", "dosage": "1 cápsula", "instructions": "Tomar de 8 em 8 horas"},
                    {"name": "Vitamina C", "dosage": "1g", "instructions": "Tomar 1 comprimido efervescente ao dia"},
                    {"name": "Descongestionante nasal", "dosage": "1 borrifada", "instructions": "Aplicar em cada narina a cada 8 horas"}
                ],
                "tosse": [
                    {"name": "Xarope de guaco", "dosage": "15ml", "instructions": "Tomar 3 vezes ao dia após as refeições"},
                    {"name": "Ambroxol", "dosage": "30mg", "instructions": "Tomar 1 comprimido 2 vezes ao dia"},
                    {"name": "Broncodilatador", "dosage": "1 dose", "instructions": "Usar 1 dose no inalador a cada 12 horas"}
                ]
            }

            medications_list = mock_medications.get(
                symptoms.lower(),
                [{"name": "Consultar especialista", "dosage": None, "instructions": "Nenhuma recomendação disponível"}]
            )

            return medications_list
        except Exception as error:
            return StatusResponseSchema(
                code=500,
                message="Erro ao simular medicações.",
                details=f"{error}"
            )