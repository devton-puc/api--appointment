from flask import jsonify
from app.logs.logger import logger
from app.route import medication_tag
from app.schemas.status import StatusResponseSchema
from app.schemas.symptoms import SymptomsSchema
from app.usecase.medication_usecase import MedicationUseCase

class MedicationRoute:

    def __init__(self):
        self.medicationUsecase = MedicationUseCase()

    def init_routes(self, app):
        @app.post('/appointment/medications/generate', tags=[medication_tag],
                  responses={
                      200: StatusResponseSchema,
                      400: StatusResponseSchema,
                      404: StatusResponseSchema,
                      500: StatusResponseSchema
                  })
        def generate_medications_route(body: SymptomsSchema):
            """Gera as medicações através dos sintomas."""
            response = self.medicationUsecase.generate_medications(body.symptoms)
            if isinstance(response, StatusResponseSchema):
                logger.debug(f"Buscando a consulta: status code [{response.code}] - mensagem: [{response.model_dump()}]")
                return jsonify(response.model_dump()), response.code
             
            medications_dict = [med.model_dump() for med in response]
            return jsonify(medications_dict), 200      