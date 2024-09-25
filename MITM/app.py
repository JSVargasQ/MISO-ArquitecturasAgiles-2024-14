from mitmproxy import http

def request(flow: http.HTTPFlow) -> None:
    # Aquí puedes interceptar y modificar las solicitudes que van de la app1 a la app2
    if flow.request.host == "127.0.0.1" and flow.request.port == 5002:
        # Intercepta las solicitudes enviadas a la app en el puerto 5002
        print(f"Interceptando solicitud a {flow.request.pretty_url}")
        
        # Modifica el cuerpo de la solicitud si es necesario
        if flow.request.method == "GET":
            # Ejemplo: modificar el body de la solicitud
            flow.request.text = flow.request.text.replace("old_data", "new_data")

def response(flow: http.HTTPFlow) -> None:
    # Intercepta y modifica las respuestas enviadas desde la app2
    if flow.response:
        print(f"Interceptando respuesta de {flow.request.pretty_url}")
        
        # Modifica el cuerpo de la respuesta si es necesario
        if flow.response.status_code == 200:
            # Ejemplo: modificar el cuerpo de la respuesta
            flow.response.text = flow.response.text.replace("response_data", "new_response_data")