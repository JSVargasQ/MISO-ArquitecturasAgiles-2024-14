import requests
from flask_restful import Resource
from flask import request
from sqlalchemy.exc import IntegrityError
from ..models import db, User, UserSchema

usuario_schema = UserSchema()

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


class PQRSManagementView(Resource):
    def post(self):
        pqrs_service_url = 'http://127.0.0.1:5002/api/v1/'

        email_user = request.json.get('user', '').strip()
        user = User.query.filter_by(email=email_user).first()

        if user:
            detail_pqrs = request.json.get('detail', '').strip()

            body_request_pqrs = {
                "user": email_user,
                "plan": user.plan,
                "type": request.json.get('type_pqrs', '').strip(),
                "detail": detail_pqrs
            }
            print(body_request_pqrs)
            try:
                response = requests.post(pqrs_service_url, json=body_request_pqrs)
                print(response)
            except:
                print("error request")

            return body_request_pqrs, 200
        else:
            return {"mensaje": "Usuario no encontrado"}, 404