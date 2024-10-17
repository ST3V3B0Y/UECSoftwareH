from flask import Blueprint, render_template, flash, request, redirect, url_for, jsonify
from flask import send_file
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
from openpyxl import Workbook
from datetime import datetime
import os
from app.models import Historial
from app.models import Equipo
from app.models import Usuario
from app.models import Software
from app.models import Facultad


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
            return render_template('administracion/historial/index.html',historial=el_historial)
    else:
        return redirect(url_for('usuario.login_administracion'))


import os
from datetime import datetime
from flask import jsonify, request
from openpyxl import Workbook

@bp.route("/historial/generar_informe", methods=["POST"])
def generar_informe():
    data = request.json
    fechaInicio = data.get('fechaInicio')
    fechaFinal = data.get('fechaFin')

    if not fechaInicio or not fechaFinal:
        return jsonify({"status": "error", "message": "Las fechas no pueden ser vacías."}), 400

    fechaInicio = datetime.strptime(fechaInicio, '%Y-%m-%d')
    fechaFinal = datetime.strptime(fechaFinal, '%Y-%m-%d')

    el_historial = db.session.query(
        Usuario.nombreUsuario,
        Usuario.identificacionUsuario,
        Facultad.nombreFacultad,
        Equipo.idEquipo,
        Historial.horaInicio,
        Historial.horaFin,
        Historial.fecha,
        Historial.nombreSala,
        Software.nombreSoftware,
        Historial.otroSoftware
        ).join(Usuario, Historial.Usuario_idUsuario == Usuario.idUsuario) \
        .join(Equipo, Historial.Equipo_idEquipo == Equipo.idEquipo) \
        .join(Software, Historial.software_idSoftware == Software.idSoftware) \
        .join(Facultad, Usuario.Facultad_idFacultad == Facultad.idFacultad) \
        .filter(Historial.horaFin.isnot(None)) \
        .filter(Historial.fecha.between(fechaInicio, fechaFinal)) \
        .all()

    # Crear un nuevo libro de trabajo de Excel
    wb = Workbook()
    ws = wb.active

    # Agregar encabezados
    ws.append([
        "Nombre Usuario", "Identificación", "Facultad", "ID Equipo", 
        "Hora Inicio", "Hora Fin", "Fecha", "Nombre Sala", "Nombre Software", "Otro Software"
    ])

    # Agregar los registros
    for registro in el_historial:
        ws.append(list(registro))

    # Generar el nombre del archivo con la fecha actual
    fecha_actual = datetime.now().strftime('%d-%m-%y')
    documentos_path = os.path.join(os.path.expanduser('~'), 'Documents')
    nombre_archivo = os.path.join(documentos_path, f'informe {fecha_actual}.xlsx')

    # Verificar si el archivo ya existe
    contador = 1
    while os.path.exists(nombre_archivo):
        nombre_archivo = os.path.join(documentos_path, f'informe {fecha_actual} ({contador}).xlsx')
        contador += 1

    # Guardar el archivo Excel
    try:
        wb.save(nombre_archivo)
        return jsonify({"status": "success", "message": f"Reporte creado exitosamente en la carpeta 'Documentos'."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al crear el reporte: {str(e)}"})