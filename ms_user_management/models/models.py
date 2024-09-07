from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import func

db = SQLAlchemy()

class User (db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(15), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    event_status = db.Column(db.String(50), nullable=False)  # e.g., "completed", "abandoned"
    event_type = db.Column(db.String(50), nullable=False)  # e.g., "inbound", "outbound"
    evnt_priority = db.Column(db.String(20), nullable=True)  # e.g., "low", "medium", "high"
   

class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_relationships = False
        load_instance = True