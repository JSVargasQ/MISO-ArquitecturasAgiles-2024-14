from celery import Celery
import requests
import os

REDIS_SERVER_URL='redis://localhost:6379/0'
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='health_check_log')
def health_check_log(data):
    call_micro_url = f"http://127.0.0.1:5000/monitor"  # Reemplaza con la URL correcta
    requests.post(call_micro_url, json=data)

@celery_app.task(name='monitor_calls_logs')
def monitor_log(data):
    with open('ms_call_handling/tasks/monitor_calls_logs.txt', 'a+') as file:
        file.write(f'{data}\n')