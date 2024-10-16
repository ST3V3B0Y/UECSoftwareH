from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from app import db
from sqlalchemy import or_
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

@bp.route("/historial", methods=['GET','POST'])
def indexHistorial():
    if current_user.is_authenticated:
        if request.method=='POST':
            persona_a_buscar = request.form.get('usuario')
            el_historial = (
                db.session.query(Usuario.nombreUsuario, Usuario.identificacionUsuario, Equipo.idEquipo, Historial.horaInicio, Historial.horaFin, Historial.fecha, Historial.nombreSala, Historial.Usuario_idUsuario, Software.nombreSoftware, Historial.otroSoftware)
                .join(Historial, Historial.Usuario_idUsuario == Usuario.idUsuario)
                .join(Equipo, Historial.Equipo_idEquipo == Equipo.idEquipo)
                .join(Software, Historial.software_idSoftware == Software.idSoftware)
                .filter(Historial.horaFin.isnot(None))
                .filter(
                    or_(
                        Equipo.idEquipo==persona_a_buscar,  # Filtra por ID de equipo con coincidencia exacta
                        Usuario.nombreUsuario.ilike(f"%{persona_a_buscar}%"),
                        Usuario.identificacionUsuario == persona_a_buscar  # Filtra por identificación exacta
                    )
                ).all()
            )
            print("consulta para buscar", el_historial)
            return render_template("administracion/historial/index.html", historial=el_historial)
        if request.method=='GET':
            el_historial = (
                db.session.query(Usuario.nombreUsuario, Usuario.identificacionUsuario, Equipo.idEquipo, Historial.horaInicio, Historial.horaFin, Historial.fecha, Historial.nombreSala, Historial.Usuario_idUsuario, Software.nombreSoftware, Historial.otroSoftware)
                .join(Historial, Historial.Usuario_idUsuario == Usuario.idUsuario)
                .join(Equipo, Historial.Equipo_idEquipo == Equipo.idEquipo)
                .join(Software, Historial.software_idSoftware == Software.idSoftware)
                .filter(Historial.horaFin.isnot(None))
                .order_by(Historial.fecha.desc(), Historial.horaFin.desc())
                .all()
            )
            print("historial ", el_historial)
            return render_template('administracion/historial/index.html',historial=el_historial)
    else:
        return redirect(url_for('usuario.login_administracion'))