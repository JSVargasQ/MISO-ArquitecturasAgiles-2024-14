from flask_restful import Resource
from flask import request
from ms_user_management.models.models import User, UserSchema,db
from datetime import datetime
from celery import Celery
from sqlalchemy.exc import IntegrityError
from ..models import db, User, UserSchema
import os
import uuid
import random
import psutil


REDIS_SERVER_URL=os.environ.get('REDIS_SERVER')
# Celery app
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name = 'health_check_log')
def register_log(*args):
    pass

@celery_app.task(name = 'monitor_logs')
def monitor_log(*args):
    pass

usuario_schema = UserSchema()

class UserManagementView(Resource):
    def post(self):
        """
        Post user event  

        """
        event_id = request.json.get('event_id', '').strip().lower()
        duration = request.json.get('duration', 0)
        event_status = request.json.get('event_status', '').strip().lower()
        event_type = request.json.get('event_type', '').strip().lower()
        event_priority = request.json.get('event_type', '').strip().lower()

        if not event_id:
            return {"message": "The field event_id is not present in the request"}, 400
        if duration == 0:
            return {"message": "The field duration is not present in the request"}, 400
        if not event_status:
            return {"message": "The field event_status is not present in the request"}, 400
        if not event_type:
            return {"message": "The field event_type is not present in the request"}, 400
        if not event_priority:
            return {"message": "The field event_priority is not present in the request"}, 400
        
        new_user = User(event_id=event_id,
                        duration=duration,
                        event_status=event_status,
                        event_type=event_type,
                        event_priority=event_priority
                        )

        try:
            
            db.session.add(new_user)
            db.session.commit()
            return UserSchema.dump(new_user), 200
        
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "El usuario ya existe o hubo un error en la creación"}, 400  
            

    def get(self, id):
        '''
        Returns one user by id
        '''
        return UserSchema.dump(User.query.get_or_404(id))
    
    
class HealthStatusView(Resource):
    def get(self, id_request):
        """
        Returns the health status of the service 
        """
        status_options = ['HEALTHY', 'UNHEALTHY', 'DEGRADED']
        
        # Get system information
        cpu_usage = psutil.cpu_percent(interval = 1) / 100
        memory_usage = psutil.virtual_memory().percent / 100
        # active_connections = len(psutil.net_connections())
        
        response_time = random.randint(30, 3000)
        service_status = random.choice(status_options)
        

        # Simular el monitoreo de múltiples APIs
        apis = [
            {"endpoint": "/api/v1/users", "statusCode": random.choice([200, 500, 503])},
            {"endpoint": "/api/v1/routing", "statusCode": random.choice([200, 500, 503])},
            {"endpoint": "/api/v1/forwarding", "statusCode": random.choice([200, 500, 503])},
            {"endpoint": "/api/v1/notifications", "statusCode": random.choice([200, 500, 503])}
        ]
        
        # Crear los resultados de monitoreo de las APIs
        check_results = []
        error_count = 0 # Contar APIs con error
        for api in apis:
            # Simular respuesta
            api_status = "OK" if api["statusCode"] == 200 else "ERROR"
            # Simular tiempo de respuesta
            response_time = random.randint(30, 100) if api_status == "OK" else random.randint(500, 1500)
            check_results.append({
                "endpoint": api["endpoint"],
                "status": api_status,
                "responseTime": response_time,  
                "statusCode": api["statusCode"]
            })
            
            if api["statusCode"] != 200:
                error_count += 1

        # Determinar el estado general del servicio según la cantidad de errores
        if error_count == 0:
            service_status = "HEALTHY"
            message = "All systems operational"
        elif error_count == 1:
            service_status = "DEGRADED"
            message = "Systems operational with minor issues"
        else:
            service_status = "UNHEALTHY"
            message = "Critical issues detected"
               
        
        # Crear respuesta
        response = {
            "type": "HEALTH_CHECK_RESPONSE",
            "timestamp": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "requestId": id_request,
            "serviceName": "calls/health",
            "status": service_status,
            "version": "0.1.15",
            "checkResults": check_results,  # Resultados de múltiples APIs
            "message": message,
            "metrics": {
                "cpu": cpu_usage,
                "memory": memory_usage
            },
        }
        
        args = response,
        register_log.apply_async(args = args, queue='health_response')
        monitor_log.apply_async(args = args, queue='monitor_logs')

        return response, 200
        