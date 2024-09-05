from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='health_check_log')
def health_check_log(data):
    with open('ms_call_handling/logs/health_check_log.txt', 'a+') as file:
        file.write(f'{data}\n')