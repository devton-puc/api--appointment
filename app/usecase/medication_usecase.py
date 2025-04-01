from app.schemas.status import StatusResponseSchema
from app.schemas.medication import MedicationSchema
import json
from app.usecase import OPENAI_TOKEN, GEMINI_AI_URL
import requests
from pydantic import BaseModel
from typing import List, Dict
from app.logs.logger import logger
import re

class Part(BaseModel):
    text: str

class Content(BaseModel):
    parts: List[Part]

class GeminiRequest(BaseModel):
    contents: List[Content]


class MedicationUseCase:
    def generate_medications(self, symptoms: str) -> StatusResponseSchema:
        try:

            response = requests.post(f"{GEMINI_AI_URL}?key={OPENAI_TOKEN}", json=self.get_gemini_request(symptoms).model_dump(), headers={"Content-Type": "application/json"})

            logger.debug(f"response: {response.json()}")

            return self.extract_response(response)
        except Exception as error:
            return StatusResponseSchema(
                code=500,
                message="Erro ao simular medicações.",
                details=f"{error}"
            )

    def get_gemini_request(self, symptoms: str): 
        return GeminiRequest(
            contents=[
                Content(
                    parts=[
                        Part(text="Faça uma indicação de remedios de acordo com o sintoma e idade."),
                        Part(text="Apenas informe o medicamento, sem a necessidade de qualquer observação."),
                        Part(text="Para o atributo instruction, informe a quantidade de ml ou comprimidos, horas e quantos dias deverá tomar o medicamento."),
                        Part(text="Responda em formato JSON na estrutura de lista [name(nome do medicamento), dosage, instructions] que seja possivel fazer parse."),
                        Part(text="Um médico está monitorando esta resposta. Não se preocupe. Seja objetivo, portanto."),
                        Part(text=f"Sintomas: {symptoms}"),
                    ]
                )
            ]
        )
    
    def extract_response(self, response)-> list[MedicationSchema] | StatusResponseSchema:
        try:
 
            response_json = response.json()            
                       
            parts_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            
            json_string = re.sub(r"```json\s*|\s*```", "", parts_text).strip()         
         
            medication_list = json.loads(json_string)
            
            medications = [
                MedicationSchema(
                    name=med.get("name"),
                    dosage=med.get("dosage"),
                    instructions=med.get("instructions")
                )
                for med in medication_list
            ]

            return medications

        except (KeyError, json.JSONDecodeError) as e:
            raise Exception(f"{type(e)} Erro ao processar a resposta da IA. Texto de entrada: {parts_text}. Erro: {e}")
