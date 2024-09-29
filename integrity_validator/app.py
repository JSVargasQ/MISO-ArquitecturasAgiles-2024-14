from datetime import datetime
import hashlib
import hmac
from celery import Celery
from flask import request
from flask_cors import CORS
from flask_restful import Api, Resource
from integrity_validator import create_app
from .models import db, Warning
import json

REDIS_SERVER_URL='redis://localhost:6379/0'
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='send_alert')
def send_alert_simulation(*args):
    # task in tasks/queue.py
    pass

app = create_app('Ingegrity Validator')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)
api = Api(app)

def calculate_hash(data):
    # Crear un objeto HMAC con la clave secreta y el mensaje
    secret_key = "clave_secreta"
    hmac_obj = hmac.new(secret_key.encode(), data.encode(), hashlib.sha256)
    # Generar el hash
    return hmac_obj.hexdigest()

class VistaValidador(Resource):
    
    def post(self):
        # Obtener el hash del encabezado
        received_hash = request.headers.get('X-Content-Hash')
        
        if not received_hash:
            return {"error": "Falta el encabezado X-Content-Hash"}, 400
        
        # Calcular el hash del cuerpo de la petición
        body = request.get_data()
        body = json.loads(body)
        
        calculated_hash = calculate_hash(body)

        
        # Comparar los hashes
        if received_hash == calculated_hash:
            return {"status": "valid", "message": "La integridad del mensaje es válida"}, 200
        else:
            alerta = Warning(timestamp=datetime.now(), message=body, hash_expected=calculated_hash, hash_received=received_hash)
            db.session.add(alerta)
            db.session.commit()
            # Simular envío de alerta
            args = f'La solicitud enviada el {alerta.timestamp} parece estar comprometida, por favor revise el registro {alerta.id} de la tabla warnings.', 
            send_alert_simulation.apply_async(args = args, queue='send_alert')

            return {"status": "invalid", "message": "La integridad del mensaje no es válida"}, 400

api.add_resource(VistaValidador, '/validator')