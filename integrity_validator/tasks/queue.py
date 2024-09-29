from celery import Celery


REDIS_SERVER_URL='redis://localhost:6379/0'
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='send_alert')
def send_alert_simulation(data):
    with open('integrity_validator/tasks/send_alert_simulation.txt', 'a+') as file:
        file.write(f'{data}\n')