from celery import Celery
import requests
import json

celery = Celery(__name__, broker='redis://localhost:6379/')

@celery.task(name='health_check')
def health_check(health_check_request):
    
    request = json.loads(health_check_request)
    
    call_micro_url = f"http://127.0.0.1:5000/api/v1/health/{request['requestId']}"  # Reemplaza con la URL correcta
    requests.get(call_micro_url)

    # user_micro_url = f"http://localhost:5001{health_check_request['checkDetails']['endpoints'][0]['path']}"  # Reemplaza con la URL correcta
    # requests.get(user_micro_url)