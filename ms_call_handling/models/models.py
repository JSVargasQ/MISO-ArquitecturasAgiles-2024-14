from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields, Schema
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Call ():
    id = db.Column(db.Integer, primary_key=True)
    pass

class CallSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Call
        include_relationships = True
        load_instance = True