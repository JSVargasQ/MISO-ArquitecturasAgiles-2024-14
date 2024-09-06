from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Call (db.Model):
    __tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    caller_id = db.Column(db.String(15), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    call_status = db.Column(db.String(50), nullable=False)  # e.g., "completed", "abandoned"
    call_type = db.Column(db.String(50), nullable=False)  # e.g., "inbound", "outbound"
    call_priority = db.Column(db.String(20), nullable=True)  # e.g., "low", "medium", "high"
   
class CallSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Call
        include_relationships = False
        load_instance = True