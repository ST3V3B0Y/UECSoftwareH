from app import db
from datetime import datetime

class Historial(db.Model):
    __tablename__ = 'historial'
    idHistorial = db.Column(db.Integer, primary_key=True)
    Usuario_idUsuario = db.Column(db.Integer, db.ForeignKey('usuario.idUsuario'), nullable=False)
    fecha = db.Column(db.Date, default=datetime.now().date(), nullable=False)
    horaInicio = db.Column(db.Time, nullable=False)
    horaFin = db.Column(db.Time, nullable=True)
    Equipo_idEquipo = db.Column(db.Integer, db.ForeignKey('equipo.idEquipo'), nullable=False)
    nombreSala = db.Column(db.String(10), nullable=False)
    software_idSoftware = db.Column(db.Integer, db.ForeignKey('software.idSoftware'), nullable=False)
    otroSoftware = db.Column(db.String(265), nullable=True)