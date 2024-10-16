from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Usuario(db.Model):
    __tablename__='usuario'
    idUsuario = db.Column(db.Integer, primary_key=True)
    usuario=db.Column(db.String(256),nullable=True)
    contraseña=db.Column(db.String(256), nullable=True)
    nombreUsuario = db.Column(db.String(256), nullable=False)
    identificacionUsuario = db.Column(db.String(256), nullable=False)
    Facultad_idFacultad = db.Column(db.Integer, db.ForeignKey('facultad.idFacultad'), nullable=False)
    historiales = db.relationship('Historial', backref='usuario', lazy=True)
    #es_administrador = db.Column(db.Boolean, default=False)
        
    def __repr__(self):
        return f'{self.nombreUsuario}'

    def is_authenticated(self):
        return True  # Siempre devolvemos True porque todos los usuarios autenticados son válidos

    def is_active(self):
        return True  # Aquí puedes implementar lógica para desactivar cuentas de usuario si es necesario

    def is_anonymous(self):
        return False  # Devolvemos False porque los usuarios autenticados no son anónimos

    def get_id(self):
        return str(self.idUsuario)  # Devolvemos el ID del usuario como una cadena Unicode
    
    def set_password(self, password):
        self.contraseña = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.contraseña, password)