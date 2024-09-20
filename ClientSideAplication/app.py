import socket
import json
import psutil
import ctypes

SERVER_HOST = '10.100.103.170'  # Dirección IP del servidor
SERVER_PORT = 5000

import tkinter as tk
from PIL import Image, ImageTk  # Pillow para manejar imágenes
from pynput import mouse, keyboard
import threading

# Función para bloquear el mouse
def bloquear_mouse():
    with mouse.Listener(on_move=lambda x, y: False, on_click=lambda x, y, button, pressed: False):
        listener.join()

# Función para bloquear el teclado
def bloquear_teclado():
    with keyboard.Listener(on_press=lambda key: False):
        listener.join()

# Función para mostrar el protector de pantalla con imagen
def mostrar_protector():
    ventana = tk.Tk()
    ventana.attributes('-fullscreen', True)  # Pantalla completa

    # Cargar la imagen de fondo
    imagen = Image.open("src/images/.jpg")  # Cambia esto por la ruta de tu imagen
    imagen = imagen.resize((ventana.winfo_screenwidth(), ventana.winfo_screenheight()), Image.ANTIALIAS)  # Ajustar la imagen a la pantalla
    imagen_fondo = ImageTk.PhotoImage(imagen)

    # Crear un label que contenga la imagen
    label_fondo = tk.Label(ventana, image=imagen_fondo)
    label_fondo.place(x=0, y=0, relwidth=1, relheight=1)  # Cubrir toda la ventana

    # Evitar que se cierre con Alt+F4
    ventana.protocol("WM_DELETE_WINDOW", lambda: None)

    ventana.mainloop()

# Función para desbloquear
def desbloquear():
    global listener
    listener.stop()
    hostname = socket.gethostname()
    ipv4= socket.gethostbyname(hostname)
    info = {
        "informacion": "se desbloqueo el equipo",
        "respuesta": ipv4
    }
    return  info

# Ejecutar el bloqueo en paralelo
def ejecutar_bloqueo():
    # Bloqueamos el mouse y teclado en hilos separados
    mouse_hilo = threading.Thread(target=bloquear_mouse)
    teclado_hilo = threading.Thread(target=bloquear_teclado)

    mouse_hilo.start()
    teclado_hilo.start()

    # Mostrar el protector de pantalla
    mostrar_protector()
    # Obtener el nombre del host actual
    hostname = socket.gethostname()

# Obtener la dirección IPv4 del equipo actual
    ipv4 = socket.gethostbyname(hostname)
    info = {
        "informacion": "se bloqueo el equipo",
        "ipv4": ipv4
    }
    return info

# Iniciar el bloqueo

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes

def connect_to_server():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((SERVER_HOST, SERVER_PORT))
        print("Client Side Application")
        while True:
            try:
                data = client.recv(1024).decode()
                if not data:
                    break
                ejecutar_bloqueo()
                
                processes = get_processes()
                response = json.dumps({'action': 'processes', 'data': processes})
                client.send(response.encode())
                
                command = json.loads(data)
                if command['action'] == 'unlock':
                    desbloqueo = desbloquear()
                    response=json.dumps({'action':  'unlock', 'data': desbloqueo})

                elif command['action'] == 'lock':
                    ejecutar_bloqueo()
                    
            except json.JSONDecodeError:
                print("Error al decodificar JSON")
            except Exception as e:
                print(f"Error: {e}")    
                break
    finally:
        client.close()

if __name__ == "__main__":
    connect_to_server()
