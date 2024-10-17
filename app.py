from flask import Flask, render_template,Blueprint
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import (
    login_required,
    login_manager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy import text
from app import create_app,db
from app.models import Equipo
from app.routes import equipo_routes
from app.models import Usuario
from app.models import Facultad
from app.models import Software
from app.config import SERVER_HOST, SERVER_PORT
import os
import socket
import threading
import json
import ctypes
import signal
app = create_app()

@app.route("/")
def index():
    contraseña ="scrypt:32768:8:1$FIYhHFrUEmO0kpti$7ec6e191d345f9d1e973e5b04fcfb4a06727a291421c96653d80b4398e5afe352cf597bc82504a8f8911843d6849a877bfdacf899bc3847f8d96d0a963db0b3e"
    #registrar administrador
    administrador_existente = Usuario.query.filter_by(idUsuario=1).first()

    if not administrador_existente:
        administrador = Usuario(
            idUsuario=1,
            usuario="administrador",
            contraseña=contraseña,
            nombreUsuario="administrador",
            identificacionUsuario="1",
            Facultad_idFacultad=17
        )
        try:
            db.session.add(administrador)
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print("Error registrando administrador", e)

    facultades_list=["ADMINISTRACION DE EMPRESAS","CIENCIA DE DATOS","MATEMATICAS","ADMINISTRACION DE EMPRESAS HOTELERAS","COMUNICACION SOCIAL Y PERIODISMO","ECONOMIA","FILOSOFIA","GEOGRAFIA","GOBIERNO Y RELACIONES INTERNACIONALES","HISTORIA","PSICOLOGIA","SOCIOLOGIA","TRABAJO SOCIAL","ANTROPOLOGIA","ARQUEOLOGIA","CONTADURIA PUBLICA", "DERECHO","FIGRI","ADMINISTRATIVO"]
    for facultad in facultades_list:
        facultad_existente = Facultad.query.filter_by(nombreFacultad=facultad).first()
        if not facultad_existente:
            facultad = Facultad(
                nombreFacultad=facultad
                )
            try:
                db.session.add(facultad)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error registrando el software {facultad}", e)

    software_list = ["ADOBE CC", "SPSS", "ARCGIS", "RISK SIMULATOR", "STATA", "EVIEWS", "NVIVO"]

    for nombre in software_list:
        # Verifica si el software ya existe en la base de datos
        software_existente = Software.query.filter_by(nombreSoftware=nombre).first()

        if not software_existente:
            # Si no existe, lo registramos
            nuevo_software = Software(
                nombreSoftware=nombre
            )
            try:
                db.session.add(nuevo_software)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error registrando el software {nombre}", e)
    software=Software.query.filter_by(idSoftware=200).first()
    if not software:
        otroSoftware = db.session.execute(text('INSERT INTO Software (idSoftware, nombreSoftware) VALUES (200, :software)'),{'software': "OTRO"})
        db.session.commit()

    #registrar equipos de las salas automaticamente
    for i in range(1, 69):
        # Verifica si el equipo ya existe en la base de datos
        equipo_existente = Equipo.query.filter_by(idEquipo=i, sala="D507").first()

        if not equipo_existente:
            # Si no existe, lo creamos
            nuevo_equipo = Equipo(
                idEquipo=i,
                estadoEquipo="libre",
                sala="D507",
                ipEquipo=0
            )
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(f"Error registrando el equipo {i} en sala D507", e)


    for i in range(101,135):
        # Verifica si el equipo ya existe en la base de datos
        equipo_existente = Equipo.query.filter_by(idEquipo=i, sala="H405").first()

        if not equipo_existente:
            # Si no existe, lo creamos
            nuevo_equipo = Equipo(
                idEquipo=i,
                estadoEquipo="libre",
                sala="H405",
                ipEquipo=0
            )
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Error registrando el equipo {i} en sala H405")


    for i in range(201,225):
        # Verifica si el equipo ya existe en la base de datos
        equipo_existente = Equipo.query.filter_by(idEquipo=i, sala="I408").first()

        if not equipo_existente:
            # Si no existe, lo creamos
            nuevo_equipo = Equipo(
                idEquipo=i,
                estadoEquipo="libre",
                sala="I408",
                ipEquipo=0
            )
            try:
                db.session.add(nuevo_equipo)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(f"Error registrando el equipo {i} en sala I408")

    return render_template('index.html')



with app.app_context():
    Base = declarative_base()
    target_metadata = db.metadata
    db.create_all()

if __name__ == '__main__':


    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
