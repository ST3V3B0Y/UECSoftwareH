from flask import Blueprint, render_template, flash, request, jsonify,redirect, url_for
from flask_login import (
    login_required,
    login_manager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
)
from sqlalchemy.exc import IntegrityError
from app import db, login_manager
from app.models import Software
bp = Blueprint("software", __name__)

@bp.route("/software",  methods=["GET"])
def indexSoftware():
    if current_user.is_authenticated:
        if request.method=="GET":
            softwares = Software.query.all()
            print("softwares: ", softwares)
            return render_template("/administracion/software/index.html", software=softwares)
    else:
        flash("Inicie sesion para continuar...", "error")
        return redirect(url_for('usuario.login_administracion'))
    
@bp.route("/software/eliminar", methods=["POST"])
def eliminar_software():
    if current_user.is_authenticated:
        if request.method == "POST":
            data = request.get_json()  # Recibir los datos en JSON
            idSoftware = data.get("idSoftware")  # Obtener el ID del software
            
            # Buscar el software por su ID
            software = Software.query.filter_by(idSoftware=idSoftware).first()
            
            if software:
                try:
                    db.session.delete(software)  # Eliminar el registro
                    db.session.commit()  # Confirmar los cambios
                    return jsonify({"status": "success", "message": f"Software eliminado correctamente."})
                except Exception as e:
                    db.session.rollback()  # Revertir los cambios si ocurre un error
                    return jsonify({"status": "error", "message": f"Error al eliminar software: {str(e)}"})
            else:
                return jsonify({"status": "error", "message": f"Software con ID {idSoftware} no encontrado."})
    
        
@bp.route("/software/nuevo", methods=["POST"])
def nuevo_software():
    if current_user.is_authenticated:
        if request.method == "POST":
            data = request.get_json()  # Recibir los datos en JSON
            nombreSoftware = data.get("nombreSoftware")  # Obtener el nombre del software
            software = Software.query.filter_by(nombreSoftware=nombreSoftware).first()
            if not software:
                try:
                    software = Software(nombreSoftware=nombreSoftware)
                    db.session.add(software)
                    db.session.commit()
                    return jsonify({"status": "success", "message": f"Software agregado correctamente."})
                except Exception as e:
                    db.session.rollback()
                    return jsonify({"status": "error", "message": f"Error al agregar software "})
            else:
                return jsonify({"status": "error", "message": f"El software {nombreSoftware}  ya existe."})


