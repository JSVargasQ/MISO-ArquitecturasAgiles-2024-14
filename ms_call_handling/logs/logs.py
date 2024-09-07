from celery import Celery
import requests
import os

REDIS_SERVER_URL=os.environ.get('REDIS_SERVER')
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='health_check_log')
def health_check_log(data):
    call_micro_url = f"http://127.0.0.1:5012/monitor"  # Reemplaza con la URL correcta
    requests.post(call_micro_url, json=data)

@celery_app.task(name='monitor_logs')
def monitor_log(data):
    with open('ms_call_handling/logs/monitor_logs.txt', 'a+') as file:
        file.write(f'{data}\n')