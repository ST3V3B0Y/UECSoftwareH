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
from datetime import datetime
from app.models import Equipo
from app.models import Historial
from app.models import Usuario
import socket
import json
import threading
from app.config import SERVER_HOST, SERVER_PORT

bp = Blueprint("equipo", __name__)

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    HOST = SERVER_HOST  # Asegúrate de que esté escuchando en todas las interfaces de red
    PORT = SERVER_PORT
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor escuchando en {HOST}:{PORT}")
        while True:
            conn, addr = server.accept()
            print(f"Conexión establecida con {addr}")
            client_thread = threading.Thread(target=handle_client, args=(conn, addr, 'unlock'))
            client_thread.start()
    except Exception as e:
        print(f"Error al iniciar el servidor: {e}")
    finally:
        server.close()



@bp.route("/equipo", methods=["GET", "POST"])
@login_required
def equipo():
    if request.method == "GET":
        usuario = current_user
        equipos = Equipo.query.all()
        return render_template(
            "administracion/equipo/main.html", usuario=usuario, equipos=equipos
        )

connected_clients =[]

def handle_client(conn, addr, accion):
    global connected_clients
    print(f"Conexión establecida desde {addr}")

    connected_clients.append({'ip': addr[0], 'conn': conn})
    print(f"Equipos conectados: {[client['ip'] for client in connected_clients]}")

    while True:
        print("entra a while")
        try:
            data = conn.recv(1024).decode()
            if not data:
                print(f"Cliente {addr} desconectado")
                break
            
            command = json.loads(data)

            if command['action'] == 'processes':
                print(f"Procesos recibidos desde {addr}: {command['data']}")
            
            print("antes de enviar accion")
            response = json.dumps({'action': accion })
            conn.send(response.encode())

        except json.JSONDecodeError:
            print("Error al decodificar JSON, los datos pueden estar mal formateados")
            break
        except ConnectionResetError:
            print(f"El cliente {addr} ha cerrado la conexión")
            break
        except OSError as e:
            print(f"Error en el socket: {e}")  # Captura errores de socket
            break
        except Exception as e:
            print(f"Error manejando el cliente: {e}")
            break
        finally:
            try:
                conn.close()  # Asegúrate de cerrar la conexión aquí
            except Exception as e:
                print(f"Error cerrando la conexión: {e}")

@bp.route("/equipo/pedir_equipo", methods=["GET", "POST"])
@login_required
def pedir_equipo():
    if request.method == "POST":
        pc = request.form.get("pc")
        try:
            noRepeatUser = Historial.query.filter(Historial.Usuario_idUsuario==current_user.idUsuario, Historial.horaFin==None).first()
            if noRepeatUser:
                return jsonify({"status": "warning", "message": "El usuario ya tiene asignado un equipo"})
            
            equipo = Equipo.query.filter_by(idEquipo=pc).first()
            equipo.estadoEquipo = "usado"
                
            registro = Historial(
                Usuario_idUsuario=current_user.idUsuario,
                Equipo_idEquipo=pc,
                nombreSala="D507",
            )
            db.session.add(registro)
            db.session.add(equipo)
            db.session.commit()
            
            equipo_ip = equipo.ipEquipo 
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            try:
                server.connect((equipo_ip, 5000))  # Conectar al cliente (IP del equipo)
                accion = 'unlock'
                response = json.dumps({'action': accion})
                server.send(response.encode())  # Enviar la acción al cliente
                server.close()
                return jsonify({"status": "success", "message": f"Computador {pc} registrado y desbloqueado correctamente."})
            except Exception as e:
                print(f"Error al conectar con el equipo {pc} en {equipo_ip}: {e}")
                return jsonify({"status": "error", "message": f"No se pudo conectar con el equipo {pc}."})

        except IntegrityError as e:
            print("error en registro pc: ", e)
            db.session.rollback()
            return jsonify({"status": "error", "message": "Error en registro"})


@bp.route("/equipo/estado_equipo", methods=["GET", "POST"])
def estado_equipo():
    if current_user.is_authenticated:
        if request.method == "POST":
            return "hola"
        else:
            equiposUsados = (
                db.session.query(Usuario.nombreUsuario, Usuario.identificacionUsuario, Equipo.idEquipo, Historial.horaInicio, Historial.horaFin, Historial.nombreSala, Historial.Usuario_idUsuario)
                .join(Historial, Historial.Usuario_idUsuario == Usuario.idUsuario)
                .join(Equipo, Historial.Equipo_idEquipo == Equipo.idEquipo)
                .filter(Historial.horaFin == None)
                .all()
            )
            cantidadEquipos = len(equiposUsados)
            return render_template("administracion/estadoEquipo/index.html", equipos_usados=equiposUsados, cantidad_equipos=cantidadEquipos)
    else:
        return redirect(url_for('usuario.login_administracion'))
    
@bp.route("/equipo/liberar_equipo/<int:idEquipo>", methods=["POST"])
def liberar_equipo(idEquipo):
    if current_user.is_authenticated:
        data = request.json  # Obtenemos el cuerpo JSON de la petición
        idUsuario = data.get('idUsuario')
        equipo_a_editar = Equipo.query.filter_by(idEquipo=idEquipo).first()  # Busca el equipo
        editar_historial = Historial.query.filter_by(Usuario_idUsuario=idUsuario, Equipo_idEquipo=idEquipo).first_or_404()
        
        # Actualizamos los campos
        equipo_a_editar.estadoEquipo = "libre"
        editar_historial.horaFin = datetime.now()
        
        try:
            db.session.commit()  # Guardamos los cambios en la base de datos
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
            historial.horaFin = datetime.now()
            
        
        try:
            db.session.commit()  # Guardamos los cambios en la base de datos
            return jsonify({'success': True, 'message': 'Historial actualizado con la fecha y hora actuales.'})
        except Exception as e:
            db.session.rollback()  # Revertimos en caso de error
            print("error en la actualizacion: ", e)
            return jsonify({'success': False, 'message': 'Error al actualizar el historial.'})
    else:
        return jsonify({'success': False, 'message': 'No estás autenticado.'})

