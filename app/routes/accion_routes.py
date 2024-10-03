from flask import Blueprint, render_template, request, jsonify, redirect,url_for
from app import db
from app.models import Equipo
from flask_login import (
    login_required,
    login_manager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
)
from sqlalchemy.exc import IntegrityError

bp = Blueprint("accion", __name__)  

@login_required
@bp.route("/accion", methods=["GET","POST"])
def redireccion():
        accion = request.form.get('action')
        if accion == "facultades":
            return redirect("https://www.uexternado.edu.co/facultades/")
        elif accion == "historial":
            return redirect(url_for('historial.indexHistorial'))
        elif accion == "estadoEquipo":
            return redirect(url_for('equipo.estado_equipo'))
        elif accion == "usuarios":
            return redirect(url_for('usuario.indexUsuario'))
        elif accion == "software":
            return redirect(url_for('software.indexSoftware'))
        




@bp.route("/D507")
def D507():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # Calcular el número de elementos a omitir y limitar el número de elementos
    offset = (page - 1) * per_page
    equipos_query = Equipo.query.filter_by(sala="D507").offset(offset).limit(per_page).all()

    # Contar el total de elementos para calcular la paginación
    total = Equipo.query.filter_by(sala="D507").count()

    return render_template("/prueba/salaD507.html", equipos=equipos_query, page=page, per_page=per_page, total=total)



@bp.route("/D507_data")
def D507_data():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '', type=str)
    estado = request.args.get('estado', '', type=str)

    # Calcular el número de elementos a omitir y limitar el número de elementos
    offset = (page - 1) * per_page

    # Construir la consulta con las condiciones adicionales
    query = Equipo.query.filter_by(sala="D507")
    if search:
        query = query.filter(Equipo.idEquipo.ilike(f"%{search}%"))
    if estado:
        query = query.filter_by(estadoEquipo=estado)

    equipos_query = query.offset(offset).limit(per_page).all()
    total = query.count()

    items = [{'idEquipo': e.idEquipo, 'estadoEquipo': e.estadoEquipo} for e in equipos_query]

    return jsonify({
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page * per_page < total else None
    })
    
    
@bp.route("/H405")
def H405():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    offset = (page - 1) * per_page
    equipos_query = Equipo.query.filter_by(sala="H405").offset(offset).limit(per_page).all()
    total = Equipo.query.filter_by(sala="H405").count()

    return render_template("/prueba/salaH405.html", equipos=equipos_query, page=page, per_page=per_page, total=total)


@bp.route("/H405_data")
def H405_data():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '', type=str)
    estado = request.args.get('estado', '', type=str)

    offset = (page - 1) * per_page

    query = Equipo.query.filter_by(sala="H405")
    if search:
        query = query.filter(Equipo.idEquipo.ilike(f"%{search}%"))
    if (estado):
        query = query.filter_by(estadoEquipo=estado)

    equipos_query = query.offset(offset).limit(per_page).all()
    total = query.count()

    items = [{'idEquipo': e.idEquipo, 'estadoEquipo': e.estadoEquipo} for e in equipos_query]

    return jsonify({
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page * per_page < total else None
    })

@bp.route("/I408")
def I408():
    page = request.args.get('page', 1, type=int)
    per_page = 10

    offset = (page - 1) * per_page
    equipos_query = Equipo.query.filter_by(sala="I408").offset(offset).limit(per_page).all()
    total = Equipo.query.filter_by(sala="I408").count()

    return render_template("/prueba/salaI408.html", equipos=equipos_query, page=page, per_page=per_page, total=total)


@bp.route("/I408_data")
def I408_data():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    search = request.args.get('search', '', type=str)
    estado = request.args.get('estado', '', type=str)

    offset = (page - 1) * per_page

    query = Equipo.query.filter_by(sala="I408")
    if search:
        query = query.filter(Equipo.idEquipo.ilike(f"%{search}%"))
    if (estado):
        query = query.filter_by(estadoEquipo=estado)

    equipos_query = query.offset(offset).limit(per_page).all()
    total = query.count()

    items = [{'idEquipo': e.idEquipo, 'estadoEquipo': e.estadoEquipo} for e in equipos_query]

    return jsonify({
        'items': items,
        'total': total,
        'page': page,
        'per_page': per_page,
        'has_prev': page > 1,
        'has_next': page * per_page < total,
        'prev_num': page - 1 if page > 1 else None,
        'next_num': page + 1 if page * per_page < total else None
    })



@bp.route("/celular")
def celular():
    return render_template("prueba/prueba_diseño_celular.html")

@bp.route("/computo")
def computo():
    return render_template("prueba/computo.html")



