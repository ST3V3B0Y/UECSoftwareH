from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from app import db
from flask_login import (
    login_required,
    login_manager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
)
from app.models import Historial
from app.models import Equipo
from app.models import Usuario
from app.models import Software


bp = Blueprint("historial", __name__)

@bp.route("/historial")
def indexHistorial():
    if current_user.is_authenticated:
        el_historial = (
                db.session.query(Usuario.nombreUsuario, Usuario.identificacionUsuario, Equipo.idEquipo, Historial.horaInicio, Historial.horaFin, Historial.nombreSala, Historial.Usuario_idUsuario, Software.nombreSoftware, Historial.otroSoftware)
                .join(Historial, Historial.Usuario_idUsuario == Usuario.idUsuario)
                .join(Equipo, Historial.Equipo_idEquipo == Equipo.idEquipo)
                .join(Software, Historial.software_idSoftware == Software.idSoftware)
                .filter(Historial.horaFin.isnot(None))
                .all()
        )
        print("historial ", el_historial)
        return render_template('administracion/historial/index.html',historial=el_historial)
    else:
        return redirect(url_for('usuario.login_administracion'))