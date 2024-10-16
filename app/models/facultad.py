from app import db

class Facultad(db.Model):
    __tablename__='facultad'
    idFacultad = db.Column(db.Integer, primary_key=True)
    nombreFacultad = db.Column(db.String(256), nullable=False)
    usuarios = db.relationship('Usuario', backref='facultad', lazy=True)