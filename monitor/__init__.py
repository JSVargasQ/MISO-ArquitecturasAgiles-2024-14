from flask import Flask
import os

def create_app(config_name):
    app = Flask(__name__)
    # SQL Alchemy ORM
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///monitoring.db'
    #app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('MONITORING_DB_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Exceptions
    app.config['PROPAGATE_EXCEPTIONS']=True
    return app

