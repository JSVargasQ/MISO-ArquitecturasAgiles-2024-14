from apscheduler.schedulers.background import BackgroundScheduler
from celery import Celery
from flask_restful import Api, Resource
from datetime import datetime
from .models import db, Monitoreo
from monitor import create_app
from threading import Thread
from flask_cors import CORS
from flask import request
import logging
import json

# Configurar logging
logging.basicConfig(level=logging.INFO)

celery = Celery(__name__, broker='redis://localhost:6379/0')

app = create_app('Monitor')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

counter = 0

@celery.task(name='health_check')
def health_check(health_check_request):
    # task in queue.py
    pass

class VistaMonitor(Resource):

    def post(self):
        health_check_response_data = request.json
        monitoreo = Monitoreo.query.filter_by(id=health_check_response_data['requestId']).first()
        
        # Calls Handling HECTOR
        if health_check_response_data['serviceName'] == 'calls/health':
            monitoreo.call_micro_response = json.dumps(health_check_response_data)
            monitoreo.call_micro_response_time = datetime.now()
            monitoreo.call_micro_response_status = health_check_response_data['status']
       
        # UserManagement PUBLIO
        elif health_check_response_data['serviceName'] == 'users/health':
            monitoreo.user_micro_response = json.dumps(health_check_response_data)
            monitoreo.user_micro_response_time = datetime.now()
            monitoreo.user_micro_response_status = health_check_response_data['status']
        db.session.add(monitoreo)
        db.session.commit()

        return {"message": "Health check response received"}, 200
    
cors = CORS(app)
api = Api(app)
api.add_resource(VistaMonitor, '/monitor')

def monitoring():
    global counter
    if counter < 100: # Contador de ejecuciones
        counter += 1
        logging.info(f"Iteración {counter}")
    else:
        sched.shutdown()  # Detiene el scheduler después de las ejecuciones

    with app.app_context():
        # Crear request
        healt_check_request_time = datetime.now()
        monitoreo = Monitoreo(healt_check_request_time=healt_check_request_time)
        db.session.add(monitoreo)
        db.session.commit()

        health_check_request = {
            "type": "HEALTH_CHECK",
            "timestamp": f"{healt_check_request_time}",
            "requestId": f"{monitoreo.id}",
            "checkDetails": {
                "endpoints": [
                    {
                        "path": "/health",
                        "method": "GET"
                    }
                ],
                "timeout": 5000
            }
        }
        health_check_request_str = json.dumps(health_check_request)
        monitoreo.healt_check_request = health_check_request_str
        db.session.add(monitoreo)
        db.session.commit()

        # Enviar request
        health_check.apply_async(args=[health_check_request_str], queue='health_check')


# Crear el scheduler
sched = BackgroundScheduler()

# Programar la función para que se ejecute cada 20 segundos
sched.add_job(monitoring, 'interval', seconds = 2)

# Iniciar el scheduler
sched.start()

# Función para iniciar el servidor Flask
def start_server():
    logging.info("Iniciando el servidor Flask")
    app.run(debug=True)
    logging.info("Servidor iniciado")

if __name__ == "__main__":
    # Iniciar el servidor Flask en un hilo separado
    server_thread = Thread(target=start_server)
    server_thread.start()