from flask_openapi3 import OpenAPI, Info, APIBlueprint
from flask_cors import CORS

from app.model import init_db
from app.route.appointment_route import AppointmentRoute
from app.route.medication_route import MedicationRoute

info = Info(title="Appointment API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

init_db()

AppointmentRoute().init_routes(app)
MedicationRoute().init_routes(app)