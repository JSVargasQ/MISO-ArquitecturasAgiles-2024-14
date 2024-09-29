import json
import re
from mitmproxy import http
from celery import Celery


REDIS_SERVER_URL='redis://localhost:6379/0'
celery_app = Celery(__name__, broker=f'{REDIS_SERVER_URL}')

@celery_app.task(name='original_request')
def original_request(*args):
    # task in tasks/queue.py
    pass

@celery_app.task(name='modified_request')
def modified_request(*args):
    # task in tasks/queue.py
    pass


def request(flow: http.HTTPFlow) -> None:
    
    # Aquí puedes interceptar y modificar las solicitudes que van de la app1 a la app2
    if flow.request.host == "127.0.0.1" and flow.request.port == 5002:
        # Intercepta las solicitudes enviadas a la app en el puerto 5002
        print(f"Interceptando solicitud a {flow.request.pretty_url}")
                    
        # Modifica el cuerpo de la solicitud si es un POST
        if flow.request.method == "POST":
            # Intenta convertir el cuerpo a un objeto JSON
            try:
                # Carga el texto de la solicitud como un objeto JSON
                data = json.loads(flow.request.text) 
                data_original = data
                                                 
                             
                # Realiza las modificaciones necesarias
                patron = r"(Baja|Media|Alta)"
                data = re.sub(patron, "Editada", data)
                
                # Convierte de nuevo el objeto JSON a texto y lo asigna al cuerpo de la solicitud
                flow.request.text = json.dumps(data, sort_keys=True, ensure_ascii=False)

                original_request.apply_async(args = (data_original,), queue='original_request')
                modified_request.apply_async(args = (data,), queue='modified_request')
    
    
            except json.JSONDecodeError:
                print("Error al decodificar el JSON en la solicitud.")

            

# def response(flow: http.HTTPFlow) -> None:
#     # Intercepta y modifica las respuestas enviadas desde la app2
#     if flow.response:
#         print(f"Interceptando respuesta de {flow.request.pretty_url}")
        
#         # Modifica el cuerpo de la respuesta si es necesario
#         if flow.response.status_code == 200:
#             # Ejemplo: modificar el cuerpo de la respuesta
#             flow.response.text = flow.response.text.replace("response_data", "new_response_data")