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
