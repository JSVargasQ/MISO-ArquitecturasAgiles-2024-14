from celery import Celery
import requests
import json
import os

REDIS_SERVER_URL=os.environ.get('REDIS_SERVER')
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='health_check')
def health_check(health_check_request):
    
    request = json.loads(health_check_request)
    
    # Call Handling Microservice
    call_micro_url = f"http://127.0.0.1:5001/api/v1/health/{request['requestId']}"  # Reemplaza con la URL correcta
    requests.get(call_micro_url)

    # User Management Microservice

    # user_micro_url = f"http://localhost:5001{health_check_request['checkDetails']['endpoints'][0]['path']}"  # Reemplaza con la URL correcta
    # requests.get(user_micro_url)