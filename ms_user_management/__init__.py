from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    
    # SQL Alchemy ORM
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abcall.db'
    app.config['SQLALCHEMY_TRACK_MODIFICACIONS'] = False
    
    # Exceptions
    app.config['PROPAGATE_EXCEPTIONS']=True
    return app