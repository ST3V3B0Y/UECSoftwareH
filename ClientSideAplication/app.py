import socket
import json
import psutil
import ctypes

#SERVER_HOST = '10.100.103.142'  # Dirección IP del servidor
SERVER_HOST = '10.33.0.93'
SERVER_PORT = 5040
#SERVER_PORT = 5040

import tkinter as tk
#from PIL import Image, ImageTk  # Pillow para manejar imágenes
#from pynput import mouse, keyboard
import threading



def bloquear_mouse():
    with mouse.Listener(on_move=lambda x, y: False, on_click=lambda x, y, button, pressed: False) as listener:
        listener.join()

# Función para bloquear el teclado
def bloquear_teclado():
    with keyboard.Listener(on_press=lambda key: False) as listener:
        listener.join()

# Función para mostrar el protector de pantalla con imagen
def mostrar_protector():
    ventana = tk.Tk()
    ventana.attributes('-fullscreen', True)  # Pantalla completa

    # Cargar la imagen de fondo
    imagen = Image.open("src/images/tu_imagen.jpg")  # Cambia esto por la ruta de tu imagen
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

# Ejecutar el bloqueo en paralelo
def ejecutar_bloqueo():
    # Bloqueamos el mouse y teclado en hilos separados
    mouse_hilo = threading.Thread(target=bloquear_mouse)
    teclado_hilo = threading.Thread(target=bloquear_teclado)

    mouse_hilo.start()
    teclado_hilo.start()

    # Mostrar el protector de pantalla
    mostrar_protector()


# Iniciar el bloqueo

def get_processes():
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        processes.append(proc.info)
    return processes

def connect_to_server():
    client = None
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER_HOST, SERVER_PORT))
        print("Client Side Application")
        while True:
            try:
                data = client.recv(1024).decode()
                if not data:
                    break
                ejecutar_bloqueo()
                
                
                command = json.loads(data)
                if command['action'] == 'unlock':
                    desbloqueo = desbloquear()
                    response=json.dumps({'action':  'unlock', 'data': desbloqueo})

                elif command['action'] == 'lock':
                    ejecutar_bloqueo()
                    
                processes = get_processes()
                response = json.dumps({'action': 'processes', 'data': processes})
                client.send(response.encode())
            except json.JSONDecodeError:
                print("Error al decodificar JSON")
            except Exception as e:
                print(f"Error: {e}")    
                break
    except socket.error as e:
        print(f"Error al crear o conectar el socket: {e}")
    finally:
        if client is not None:  # Verifica si el socket fue creado
            client.close()  # Cierra el socket solo si fue creado

if __name__ == "__main__":
    connect_to_server()
