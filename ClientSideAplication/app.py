import socket
import json
import psutil
import ctypes

SERVER_HOST = '10.100.103.170'  # Dirección IP del servidor
SERVER_PORT = 5000

def lock_screen():
    ctypes.windll.user32.LockWorkStation()

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
                command = json.loads(data)
                if command['action'] == 'lock_screen':
                    lock_screen()
                elif command['action'] == 'get_processes':
                    processes = get_processes()
                    response = json.dumps({'action': 'processes', 'data': processes})
                    client.send(response.encode())
            except json.JSONDecodeError:
                print("Error al decodificar JSON")
            except Exception as e:
                print(f"Error: {e}")    
                break
    finally:
        client.close()

if __name__ == "__main__":
    connect_to_server()
