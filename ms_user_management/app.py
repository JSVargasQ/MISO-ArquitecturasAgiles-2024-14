from ms_user_management import create_app
from flask_restful import Api
from .models import db
from .views import  UserManagementView,HealthStatusView
from flask_cors import CORS

app = create_app('User Management Microservice')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

cors= CORS(app)
api = Api(app)

API_PREFIX = '/api/usermanagement'

api.add_resource(UserManagementView, f'{API_PREFIX}/users')
api.add_resource(HealthStatusView, f'{API_PREFIX}/health')
