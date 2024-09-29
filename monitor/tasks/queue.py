from celery import Celery
import requests
import json
import os

REDIS_SERVER_URL='redis://localhost:6379/0'
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='health_check')
def health_check(health_check_request):
    
    # Id de la petición 
    request = json.loads(health_check_request)
    
    # Call Handling Microservice
    call_micro_url = f"http://127.0.0.1:5001/api/v1/health/{request['requestId']}"  # Reemplaza con la URL correcta
    requests.get(call_micro_url)

    # User Management Microservice
    user_micro_url = f"http://127.0.0.1:5002/api/v1/health/{request['requestId']}"   # Reemplaza con la URL correcta
    requests.get(user_micro_url)