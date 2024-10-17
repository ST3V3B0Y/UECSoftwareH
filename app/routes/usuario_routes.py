from flask import Blueprint, render_template, flash, request, redirect, url_for
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
from werkzeug.security import check_password_hash, generate_password_hash
from flask import jsonify
from app import db, login_manager
from app.models.facultad import Facultad
from app.models.usuario import Usuario

bp = Blueprint("usuario", __name__)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Por favor inicia sesión para acceder a esta página.", "error")
    return redirect(url_for("usuario.login"))



@bp.route("/usuario", methods=['GET','POST'])
def indexUsuario():
    if current_user.is_authenticated:
        if request.method=='GET':
            usuarios = (db.session.query(Usuario.identificacionUsuario, Usuario.nombreUsuario, Facultad.nombreFacultad)
                        .join(Usuario, Usuario.Facultad_idFacultad==Facultad.idFacultad).all())
            return render_template('administracion/usuarios/usuarios.html',usuarios=usuarios)
        if request.method=='POST':
            usuario_a_buscar = request.form.get('usuario')
            usuarios = (
                db.session.query(Usuario.identificacionUsuario, Usuario.nombreUsuario, Facultad.nombreFacultad)
                .join(Facultad, Usuario.Facultad_idFacultad==Facultad.idFacultad)
                .filter(
                    or_(
                        Usuario.nombreUsuario.ilike(f"%{usuario_a_buscar}%"),
                        Usuario.identificacionUsuario == usuario_a_buscar,
                        Facultad.nombreFacultad.ilike(f"%{usuario_a_buscar}%")
                    )).all()
                )
            print("usuario a buscar",usuario_a_buscar)
            print("usuario busqueda",usuarios)
            return render_template('administracion/usuarios/usuarios.html',usuarios=usuarios)
    else:
        flash("Inicie sesion para continuar...", "error")
        return redirect(url_for('usuario.login_administracion'))



@bp.route("/register_usuario", methods=["GET", "POST"])
def register_usuario():
    if request.method == "GET":
        facultad = Facultad.query.all()
        return render_template("usuario/register_usuarios.html", facultad=facultad)
    
    if request.method == "POST":
        documento = request.form["documento"]
        nombre = request.form["nombre"]
        facultad = request.form.get('facultad')
        identificacionUsuario = Usuario.query.filter_by(identificacionUsuario=documento).count()

        if not facultad or not nombre:
            return {"status": "error", "message": "Complete todos los campos"}, 400
        elif identificacionUsuario > 0:
            return {"status": "warning", "message": "Identificación ya registrada"}, 400
        else:
            usuario = Usuario(
                usuario=None,
                contraseña=None,
                nombreUsuario=nombre,
                identificacionUsuario=documento,
                Facultad_idFacultad=facultad,
            )
            try:
                db.session.add(usuario)
                db.session.commit()
                usuarioActual = Usuario.query.filter_by(identificacionUsuario=documento).first()
                login_user(usuarioActual)
                return {"status": "success", "message": "Registro exitoso"}, 200
            except IntegrityError as e:
                db.session.rollback()
                return {"status": "error", "message": "Error en el registro"}, 400




@bp.route("/login_usuario", methods=["GET", "POST"])
def login_usuario():
    if request.method == "GET":
        return redirect(url_for('usuario.login'))
    if request.method == "POST":
        identificacion = request.form.get("documento")
        if identificacion:
            usuarioActual = Usuario.query.filter_by(
                identificacionUsuario=identificacion
            ).first()
            if usuarioActual:
                login_user(usuarioActual)
                return jsonify({"success": True, "redirect": url_for("equipo.equipo")})
            else:
                return jsonify({"success": False, "message": "Usted no está registrado en el sistema..."})
    return jsonify({"success": False, "message": "Error en la solicitud."})

    


@bp.route("/login")
def login():
    if request.method=="GET":
        return render_template("usuario/login_usuarios.html")
    
@bp.route("/login_administracion", methods=["GET","POST"])
def login_administracion():
    if request.method=="GET":
        return render_template("administracion/login_administracion.html")
    if request.method=="POST":
        usuario = request.form.get("usuario")
        contraseña = request.form.get("contraseña")
        user = Usuario.query.filter_by(usuario=usuario).first()
        #contraseña_hash = generate_password_hash(contraseña)
        #print(contraseña_hash)
        if user:
            
            if check_password_hash(user.contraseña, contraseña):
                login_user(user)
                print("current user:", current_user)
                return redirect(url_for('usuario.administracion'))
            else :
                flash("Ingrese la contraseña de administrador correcta.", "error")
                return redirect(url_for('usuario.login_administracion'))         
        else:
            flash("El usuario no existe.", "error")
            return redirect(url_for('usuario.login_administracion'))

@bp.route("/administracion", methods=["GET","POST"])
def administracion():
    if current_user.is_authenticated:
        if request.method=="GET":
            return render_template("administracion/administracion.html")
    else:
        flash("Inicie sesion para continuar...", "error")
        return redirect(url_for('usuario.login_administracion'))

        

@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@bp.route("/perfil", methods=["GET","POST"])
@login_required
def perfil():
    if request.method=="GET":
        return render_template("usuario/usuarios.html")

