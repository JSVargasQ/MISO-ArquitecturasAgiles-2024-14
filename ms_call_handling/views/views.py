from flask_restful import Resource
from datetime import datetime
import uuid
import random
import psutil

class CallHandlingView(Resource):
    def get(self):
        """
        Get and Handling calls 
        """

class HealthStatusView(Resource):
    def get(self):
        
        status_options = ['HEALTHY', 'UNHEALTHY', 'DEGRADED']
        
        # Get system information
        cpu_usage = psutil.cpu_percent(interval = 1) / 100
        memory_usage = psutil.virtual_memory().percent / 100
        # active_connections = len(psutil.net_connections())
        
        response_time = random.randint(30, 3000)
        service_status = random.choice(status_options)
        

        # Simular el monitoreo de múltiples APIs
        apis = [
            {"endpoint": "/api/v1/calls", "statusCode": random.choice([200, 500, 503])},
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
            "requestId": f"hc-{uuid.uuid4().hex[:6]}",
            "serviceName": "call-handling",
            "status": service_status,
            "version": "0.1.15",
            "checkResults": check_results,  # Resultados de múltiples APIs
            "message": message,
            "metrics": {
                "cpu": cpu_usage,
                "memory": memory_usage,
                # "activeConnections": active_connections
            },
        }

        return response, 200
    