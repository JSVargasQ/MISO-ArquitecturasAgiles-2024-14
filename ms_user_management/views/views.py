from flask_restful import Resource
from flask import request
from ms_user_management.models.models import User, UserSchema,db


usuario_schema = UserSchema()

class UserManagementView(Resource):
    def post(self):
        """
        Post user event 

        """
        nuevo_usuario = User(name=request.json["name"],  value=request.json["value"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario)

    def get(self, id):
        return UserSchema.dump(User.query.get_or_404(id))
    
    
class HealthStatusView(Resource):
    def get(self):
        """
        Returns the health status of the service 
        """
        return {"message": "Service health at 100%", "status": "ok"}, 200
        