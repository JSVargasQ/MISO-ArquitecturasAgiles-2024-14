from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Monitoreo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    healt_check_request = db.Column(db.Text, nullable=True)
    healt_check_request_time = db.Column(db.String(20), nullable=True)
    call_micro_response = db.Column(db.Text, nullable=True)
    call_micro_response_time = db.Column(db.String(20), nullable=True)
    call_micro_response_status = db.Column(db.String(10), nullable=True)
    user_micro_response = db.Column(db.Text, nullable=True)
    user_micro_response_time = db.Column(db.String(20), nullable=True)
    user_micro_response_status = db.Column(db.String(10), nullable=True)

class MonitoreoSchemas(SQLAlchemyAutoSchema):
    class Meta:
        model = Monitoreo
        load_instance = True