from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Warning (db.Model):
    __tablename__ = 'warnings'
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.String(20))
    message = db.Column(db.String(100))
    hash_expected = db.Column(db.String(100))
    hash_received = db.Column(db.String(100))