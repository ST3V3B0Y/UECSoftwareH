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
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from datetime import datetime
from app.models import Equipo
from app.models import Historial
from app.models import Usuario
from app.models import Software
import socket
import json
import threading
from app.config import SERVER_HOST, SERVER_PORT

bp = Blueprint("equipo", __name__)

@bp.route("/equipo", methods=["GET", "POST"])
@login_required
def equipo():
    if request.method == "GET":
        usuario = current_user
        equipos = Equipo.query.all()
        software = Software.query.all()
        software_list = [{"idSoftware": s.idSoftware, "nombreSoftware": s.nombreSoftware} for s in software]
        return render_template(
            "administracion/equipo/main.html", usuario=usuario, equipos=equipos, software=software_list
        )


@bp.route("/equipo/pedir_equipo", methods=["GET", "POST"])
@login_required
def pedir_equipo():
    if request.method == "POST":
        data = request.get_json()
        pc = data.get('pc')
        software_seleccionado = request.form.get('software')
        software = data.get('softwareId')
        otroSoftware = data.get('otroSoftware')

        print("Datos recibidos:", data)
        try:
            noRepeatUser = Historial.query.filter(Historial.Usuario_idUsuario==current_user.idUsuario, Historial.horaFin==None).first()
            if noRepeatUser:
                return jsonify({"status": "warning", "message": "El usuario ya tiene asignado un equipo"})

            equipo = Equipo.query.filter_by(idEquipo=pc).first()
            equipo.estadoEquipo = "usado"
            if software_seleccionado==0:
                return jsonify({"status": "warning", "message": "Por favor selecciona un software"})
            else: 
                if otroSoftware is None:
                    registro = Historial(
                    Usuario_idUsuario=current_user.idUsuario,
                    horaInicio=datetime.now().strftime('%H:%M:%S'),
                    Equipo_idEquipo=pc,
                    nombreSala="D507",
                    software_idSoftware=software
                )
                else :
                    registro = Historial(
                    Usuario_idUsuario=current_user.idUsuario,
                    horaInicio=datetime.now().strftime('%H:%M:%S'),
                    Equipo_idEquipo=pc,
                    nombreSala="D507",
                    software_idSoftware=software,
                    otroSoftware=otroSoftware
                    )
            db.session.add(registro)
            db.session.add(equipo)
            db.session.commit()

        

            return jsonify({"status": "success", "message": f"Computador {pc} registrado y desbloqueado correctamente."})
        except IntegrityError as e:
            print("error en registro pc: ", e)
            db.session.rollback()
            return jsonify({"status": "error", "message": "Complete todos los campos"})


@bp.route("/equipo/estado_equipo", methods=["GET", "POST"])
def estado_equipo():
    if current_user.is_authenticated:
        if request.method == "POST":
            equipo_a_buscar = request.form.get('equipo')
            buscar = (
                db.session.query(Usuario.nombreUsuario, Usuario.identificacionUsuario, Equipo.idEquipo, Historial.horaInicio, Equipo.sala, Software.nombreSoftware, Historial.otroSoftware, Historial.Usuario_idUsuario, Historial.fecha)
                .join(Historial, Historial.Usuario_idUsuario == Usuario.idUsuario)
                .join(Equipo, Historial.Equipo_idEquipo == Equipo.idEquipo)
                .join(Software, Historial.software_idSoftware == Software.idSoftware)
                .filter(Historial.horaFin == None)
                .filter(or_(
                    Equipo.idEquipo==equipo_a_buscar,
                    Usuario.nombreUsuario.ilike(f"%{equipo_a_buscar}%"),
                    Usuario.identificacionUsuario==equipo_a_buscar
                    )
                )
                .order_by(Historial.fecha.desc(), Historial.horaInicio.desc())
                .all()
            )
            print("consulta para buscar",buscar)
            cantidadEquipos = len(buscar)
            return render_template("administracion/estadoEquipo/index.html", equipos_usados=buscar, cantidad_equipos=cantidadEquipos)
        else:
            equiposUsados = (
                db.session.query(Usuario.nombreUsuario, Usuario.identificacionUsuario, Equipo.idEquipo, Historial.horaInicio, Equipo.sala, Software.nombreSoftware, Historial.otroSoftware, Historial.Usuario_idUsuario, Historial.fecha)
                .join(Historial, Historial.Usuario_idUsuario == Usuario.idUsuario)
                .join(Equipo, Historial.Equipo_idEquipo == Equipo.idEquipo)
                .join(Software, Historial.software_idSoftware == Software.idSoftware)
                .filter(Historial.horaFin == None)
                .order_by(Historial.fecha.desc(), Historial.horaInicio.desc())
                .all()
            )
            print("informacion de la tabla",equiposUsados)
            cantidadEquipos = len(equiposUsados)
            return render_template("administracion/estadoEquipo/index.html", equipos_usados=equiposUsados, cantidad_equipos=cantidadEquipos)
    else:
        return redirect(url_for('usuario.login_administracion'))

@bp.route("/equipo/liberar_equipo/<int:idEquipo>", methods=["POST"])
def liberar_equipo(idEquipo):
    if current_user.is_authenticated:
        data = request.json  # Obtiene el cuerpo JSON de la petición
        idUsuario = data.get('idUsuario')  # Obtiene el idUsuario

        equipo_a_editar = Equipo.query.filter_by(idEquipo=idEquipo).first()
        editar_historial = Historial.query.filter_by(Usuario_idUsuario=idUsuario, Equipo_idEquipo=idEquipo, horaFin=None).first_or_404()

        # Actualizamos los campos
        equipo_a_editar.estadoEquipo = "libre"
        editar_historial.horaFin = datetime.now().strftime('%H:%M:%S') # Actualiza la hora

        try:
            db.session.commit()
            return jsonify({'success': True, 'message': 'Historial actualizado con la fecha y hora actuales.'})
        except Exception as e:
            db.session.rollback()  # Revertimos en caso de error
            print("error en la actualizacion: ", e)
            return jsonify({'success': False, 'message': 'Error al actualizar el historial.'})
    else:
        return jsonify({'success': False, 'message': 'No estás autenticado.'})

@bp.route("/equipo/liberar_todo/", methods=["POST"])
def liberar_todo():
    if current_user.is_authenticated:
        editar_historial_D507 = Historial.query.filter(Historial.horaFin==None, Equipo.sala=="D507").all()
        editar_equipo_D507 = Equipo.query.filter(Equipo.estadoEquipo=="usado", Equipo.sala=="D507").all()

        for equipo in editar_equipo_D507:
            equipo.estadoEquipo = "libre"

        # Actualizar los campos de cada equipo y registro del historial
        for historial in editar_historial_D507:
            historial.horaFin = datetime.now().strftime('%H:%M:%S')

        try:
            db.session.commit()  # Guardamos los cambios en la base de datos
            return jsonify({'success': True, 'message': 'Historial actualizado con la fecha y hora actuales.'})
        except Exception as e:
            db.session.rollback()  # Revertimos en caso de error
            print("error en la actualizacion: ", e)
            return jsonify({'success': False, 'message': 'Error al actualizar el historial.'})
    else:
        return jsonify({'success': False, 'message': 'No estás autenticado.'})

