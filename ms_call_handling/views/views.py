from flask_restful import Resource

class CallHandlingView(Resource):
    def get(self):
        """
        Get and Handling calls 
        """

class HealthStatusView(Resource):
    def get(self):
        """
        Returns the health status of the service 
        """
        return {"message": "Service health at 100%", "status": "ok"}, 200
        