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
from werkzeug.security import check_password_hash, generate_password_hash
from app import db, login_manager
from app.models.facultad import Facultad
from app.models.usuario import Usuario

bp = Blueprint("usuario", __name__)

@login_manager.unauthorized_handler
def unauthorized_callback():
    flash("Por favor inicia sesión para acceder a esta página.", "error")
    return redirect(url_for("usuario.login"))



@bp.route("/usuario")
def indexUsuario():
    if current_user.is_authenticated:
        usuarios = Usuario.query.order_by(Usuario.idUsuario.desc()).all()
        return render_template('administracion/usuarios/usuarios.html',usuarios=usuarios)
    else:
        flash("Inicie sesion para continuar...", "error")
        return redirect(url_for('usuario.login_administracion'))

@bp.route("/register_usuario", methods=["GET", "POST"])
def register_usuario():
    if request.method == "GET":
        facultad = Facultad.query.all()
        return render_template(
            "usuario/register_usuarios.html", facultad=facultad
        )
    if request.method == "POST":
        documento = request.form["documento"]
        nombre = request.form["nombre"]
        facultad = request.form.get('facultad')
        identificacionUsuario = Usuario.query.filter_by(
            identificacionUsuario=documento
        ).count()

        if not facultad or not nombre:
            flash("Complete todos lo campos", "error")
            return redirect(url_for("usuario.register_usuario"))
        elif identificacionUsuario > 0:
            flash("identificacion ya registrada", "warning")
            return redirect(url_for("usuario.register_usuario"))
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
                login_usuario()
                flash("Registrado Correctamente", "success")
                return redirect(
                    url_for(
                        "usuario.login_usuario",
                    )
                )
            except IntegrityError as e:
                db.session.rollback()
                flash("error en registro", "error")
                print("error en el registro", e)
                return redirect(url_for("usuario.register_usuario"))


@bp.route("/login_usuario", methods=["GET","POST"])
def login_usuario():
    if request.method=="GET":
        return redirect(url_for('usuario.login'))
    if request.method=="POST":
        identificacion = request.form.get("documento")
        if identificacion:
            usuarioActual = Usuario.query.filter_by(
                identificacionUsuario=identificacion
            ).first()
            if usuarioActual:
                login_user(usuarioActual)
                print("usuario actual ",current_user)
                return redirect(url_for("equipo.equipo"))
            else :
                flash("Usted no esta registrado en el sistema...", "error")
                return redirect(url_for('usuario.login'))
    return redirect(url_for("usuario.login"))
    


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

