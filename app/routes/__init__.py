from flask import Blueprint

bp = Blueprint('main', __name__)

from app.routes import accion_routes, equipo_routes, facultad_routes, historial_routes, usuario_routes,software_routes