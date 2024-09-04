from ms_user_management import create_app
from flask_restful import Api
from .views import  UserManagementView,HealthStatusView

app = create_app('Call Handling Microservice')
app_context = app.app_context()
app_context.push()

api = Api(app)

API_PREFIX = 'api/v1'

api.add_resource(UserManagementView, f'{API_PREFIX}/users')
api.add_resource(HealthStatusView, f'{API_PREFIX}/health')
