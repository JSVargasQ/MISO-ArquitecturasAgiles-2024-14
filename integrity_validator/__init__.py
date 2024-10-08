from flask import Flask


def create_app(config_name):
    app = Flask(__name__)
    # SQL Alchemy ORM
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///validator.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Exceptions
    app.config['PROPAGATE_EXCEPTIONS']=True
    return app