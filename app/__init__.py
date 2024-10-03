from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import socket
import threading
import json
import pymysql



db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("config.py")

    init_extensions(app)
    register_blueprints(app)
    create_database_if_not_exists('disponibilidad_equipos')
    
    return app


def create_database_if_not_exists(db_name):
    conn = pymysql.connect(user='root', password='', host='localhost')
    cursor = conn.cursor()
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        print(f"Base de datos {db_name} verificada o creada.")
    except Exception as e:
        print("error al crear database ", e)

    cursor.close()
    conn.close()

# Llamar la función para crear la base de datos

def init_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'usuario.login'
    login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."
    login_manager.login_message_category = "info"
    


    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        from .models.usuario import Usuario
        return Usuario.query.get(int(user_id))


def register_blueprints(app):
    from app.routes import (accion_routes, equipo_routes, facultad_routes,historial_routes, usuario_routes,software_routes)
    app.register_blueprint(accion_routes.bp)
    app.register_blueprint(equipo_routes.bp)
    app.register_blueprint(facultad_routes.bp)
    app.register_blueprint(historial_routes.bp)
    app.register_blueprint(usuario_routes.bp)
    app.register_blueprint(software_routes.bp)
