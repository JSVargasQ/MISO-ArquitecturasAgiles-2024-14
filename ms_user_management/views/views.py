import hashlib
import hmac
import requests
import json
import random

from flask_restful import Resource
from flask import request
from faker import Faker
from sqlalchemy.exc import IntegrityError
from ..models import db, User, UserSchema
from datetime import datetime

usuario_schema = UserSchema()
faker = Faker()


class UserManagementView(Resource):
    def post(self):
        name_user = request.json.get('name', '').strip()
        lastname_user = request.json.get('lastname', '').strip()
        email_user = request.json.get('email', '').strip().lower()
        country_user = request.json.get('country', '').strip().lower()
        city_user = request.json.get('city', '').strip().lower()
        plan_user = request.json.get('plan', '').strip()

        new_user = User(name=name_user,
                        lastname=lastname_user,
                        email=email_user,
                        country=country_user,
                        city=city_user,
                        plan=plan_user
                        )

        try:

            db.session.add(new_user)
            db.session.commit()
            return usuario_schema.dump(new_user), 200

        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "El usuario ya existe o hubo un error en la creación"}, 400


class UserManagementView(Resource):
    def post(self):
        name_user = request.json.get('name', '').strip()
        lastname_user = request.json.get('lastname', '').strip()
        email_user = request.json.get('email', '').strip().lower()
        phone_user = request.json.get('phone', '').strip().lower()
        country_user = request.json.get('country', '').strip().lower()
        city_user = request.json.get('city', '').strip().lower()
        plan_user = request.json.get('plan', '').strip()

        new_user = User(
            name=name_user,
            lastname=lastname_user,
            email=email_user,
            phone=phone_user,
            country=country_user,
            city=city_user,
            plan=plan_user
        )

        try:

            db.session.add(new_user)
            db.session.commit()
            return usuario_schema.dump(new_user), 200

        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "El usuario ya existe o hubo un error en la creación"}, 400


class PQRSManagementView(Resource):
    def post(self):
        pqrs_service_url = 'http://127.0.0.1:5001/api/v1/'
        experimental_service_url = 'http://127.0.0.1:5002/api/v1/'

        created_at = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        email_user = request.json.get('user', '').strip()
        user = User.query.filter_by(email=email_user).first()

        if user:
            detail_pqrs = request.json.get('detail', '').strip()
            body_request_pqrs = {
                "contact_info": {
                    "user": email_user,
                    "phone": user.phone
                },
                "detail": detail_pqrs,
                "priority": faker.random_element(elements=["Baja", "Media", "Alta"]),
                "category": faker.random_element(elements=["Servicio al Cliente", "Soporte Técnico", "Facturación"]),
                "status": "En Proceso",
                "submitted_at": created_at,
                "type": request.json.get('type_pqrs', '').strip(),
                "user_id": user.id,
                "attachments": [
                    {
                        "filename": faker.file_name(extension='img'),
                        "file_url": faker.url()
                    },
                    {
                        "filename": faker.file_name(extension='pdf'),
                        "file_url": faker.url()
                    }
                ],
            }
            hashBody = self.createHash(body_request_pqrs)
            headers = {
                'X-Content-Hash': hashBody,
            }

            try:
                if random.random() < 0.25:
                    response = requests.post(experimental_service_url, headers=headers, json=body_request_pqrs)
                else:
                    response = requests.post(pqrs_service_url, headers=headers, json=body_request_pqrs)
                code_status = 200
            except:
                print("error request")
                response = "error in request"
                code_status = 500

            return response, code_status
        else:
            return {"mensaje": "Usuario no encontrado"}, 404

    def createHash(self, body):
        # Crear un objeto HMAC con la clave secreta y el mensaje
        secret_key = "clave_secreta"
        body = json.dumps(body)
        hmac_obj = hmac.new(secret_key.encode(), body.encode(), hashlib.sha256)
        # Generar el hash
        return hmac_obj.hexdigest()
