import json
import requests
from flask import Flask
from flask_restful import Api, Resource
import datetime
import redis
import os
import sched
import time
import threading
import random

hostRedis = os.environ.get('HOST_REDIS', 'localhost')
portRedis = os.environ.get('PORT_REDIS', 6379)

delayInterval = 5

app = Flask(__name__)
app_context = app.app_context()
app_context.push()
api = Api(app)

r = redis.StrictRedis(hostRedis, portRedis, 0, charset='utf-8', decode_responses=True)


def execute_ping_to_user_service():
    now = datetime.datetime.now().replace(microsecond=0).time()
    print('+-------START EXECUTION JOB SCHEDULER [%s]-------+' % now.strftime("%H:%M:%S"))

    numero = random.randint(1, 3)

    make_ping_to_user_service(numero)

    now = datetime.datetime.now().replace(microsecond=0).time()
    print('+-------END EXECUTION JOB SCHEDULER [%s]-------+' % now.strftime("%H:%M:%S"))

def make_ping_to_user_service(microservice_host):
    try:
        url=""
        if(microservice_host==1):
            url ="http://localhost:5000/api/usermanagement/health"

        if(microservice_host==2):
            url ="http://localhost:5001/api/usermanagement/health"

        if(microservice_host==3):
            url ="http://localhost:5008/api/usermanagement/health"

       
        print("EnPoint Service Url: "+url)        

        servicse_user_status_response = requests.get(url)
        response_text = servicse_user_status_response.text.replace('\n', '').replace('"', '')
        print('[Response host {} ] is {}'.format(microservice_host, response_text))

        json_data = json.loads(servicse_user_status_response.text)

        status = json_data['status']

        if (status == 'ok' and servicse_user_status_response.status_code == 200):
            notify_user_service_url_status("Host_"+str(microservice_host), response_text)
        else:
            notify_user_service_url_status("Host_"+str(microservice_host), "down")

    except Exception as ex:
        print("****************Failed to establish a new connection****************")
        notify_user_service_url_status("Host_down_"+str(microservice_host), str(ex))



def notify_user_service_url_status(host_name, new_host_status):
    
    try:
        now = datetime.datetime.now().replace(microsecond=0).time()
        formatted_time = now.strftime("%H_%M_%S")
        
        r.set(host_name+":"+formatted_time, str(new_host_status))
        print('NOTIFY SERVICE_USER CHANGE STATE Host ={} status= {}'.format(host_name, new_host_status))

    except Exception as ex:
        print('[Notify Status] error {}'.format(str(ex)))


def loop_task():
    execute_ping_to_user_service()
    scheduler.enter(delayInterval, 1, loop_task, ())


class MonitorHealthResource(Resource):
    def get(self):
        return {"status": "OK"}


api.add_resource(MonitorHealthResource, '/monitor/health-check')


scheduler = sched.scheduler(time.time, time.sleep)


def run_scheduler():
    loop_task()
    scheduler.run()


if __name__ == '__main__':
    threading.Timer(5, run_scheduler).start()
    app.run(debug=False, host='0.0.0.0', port=os.environ.get('PORT', 5003))
