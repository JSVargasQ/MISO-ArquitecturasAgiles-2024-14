from flask import Flask,jsonify
import requests
from faker import Faker

app = Flask(__name__)
faker = Faker()


# URL del endpoint Flask (asume que está corriendo en localhost)
url = 'http://127.0.0.1:5000/pqr'

@app.get('/pqrs')
def get_pqrs():
    # Lista para almacenar los resultados de las PQRs
    pqrs_list = []

    # Hacer 5 solicitudes al endpoint y almacenar los resultados
    for i in range(5):
        response = requests.get(url)
        
        if response.status_code == 200:
            pqr_data = response.json()
            pqrs_list.append(pqr_data)
        else:
            print(f"Error en la solicitud {i+1}: {response.status_code}")
    # Usamos jsonify para devolver el array de objetos en formato JSON
    return jsonify(pqrs_list), 200

@app.get('/pqr')
def get_pqr():
    return {
        "user_id": faker.random_int(min=1000, max=9999),
        "type": faker.random_element(elements=["Petición", "Queja", "Reclamo"]),
        "description": faker.text(max_nb_chars=100),
        "contact_info": {
            "email": faker.email(),
            "phone": faker.phone_number()
        },
            "priority": faker.random_element(elements=["Baja", "Media", "Alta"]),
            "attachments": [
                {
                    "filename":  faker.file_name(extension='img'),
                    "file_url": faker.url()
                },
                {
                    "filename": faker.file_name(extension='pdf'),
                    "file_url": faker.url()
                }
            ],
            "category": faker.random_element(elements=["Servicio al Cliente", "Soporte Técnico", "Facturación"]),
            "status": faker.random_element(elements=["Pendiente", "Resuelto", "En Proceso"]),
            "submitted_at": faker.iso8601()
        }
