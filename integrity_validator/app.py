from datetime import datetime
import hashlib
from flask import jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from integrity_validator import create_app
from .models import db

app = create_app('Ingegrity Validator')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors = CORS(app)
api = Api(app)

def calculate_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

class VistaValidador(Resource):
    
    def post(self):
        # Obtener el hash del encabezado
        received_hash = request.headers.get('X-Content-Hash')
        
        if not received_hash:
            return jsonify({"error": "Falta el encabezado X-Content-Hash"}), 400
        
        # Calcular el hash del cuerpo de la petición
        body = request.get_data(as_text=True)
        calculated_hash = calculate_hash(body)
        
        # Comparar los hashes
        if received_hash == calculated_hash:
            return jsonify({"status": "valid", "message": "La integridad del mensaje es válida"}), 200
        else:
            alerta = Warning(timestamp=datetime.now(), message=body, hash_expected=calculated_hash, hash_received=received_hash)
            db.session.add(alerta)
            db.session.commit()
            # TODO: Simular envío de notificación por una cola
            return jsonify({"status": "invalid", "message": "La integridad del mensaje no es válida"}), 400

api.add_resource(VistaValidador, '/validator')