from app import db

class Equipo(db.Model):
    __tablename__='equipo'
    idEquipo = db.Column(db.Integer, primary_key=True)
    estadoEquipo = db.Column(db.String(256), nullable=False)
    sala=db.Column(db.String(5), nullable=False)
    ipEquipo=db.Column(db.String(30), nullable=False)
    
    def __repr__(self):
        return f'{self.estadoEquipo}'
