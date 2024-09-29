from celery import Celery


REDIS_SERVER_URL='redis://localhost:6379/0'
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='original_request')
def original_request(data):
    with open('MITM/tasks/original_request.txt', 'a+') as file:
        file.write(f'{data}\n')

@celery_app.task(name='modified_request')
def modified_request(data):
    with open('MITM/tasks/modified_request.txt', 'a+') as file:
        file.write(f'{data}\n')