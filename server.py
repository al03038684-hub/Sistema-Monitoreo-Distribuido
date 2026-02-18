import socket
import threading
import psutil
import subprocess
import os

HOST = '0.0.0.0'
PORT = 6000

def handle_client(conn, addr):
    print(f"Conectado a {addr}")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break

        command = data.split()

        if command[0] == "LIST":
            processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                processes.append(f"{proc.info['pid']} - {proc.info['name']}")
            response = "\n".join(processes)

        elif command[0] == "START":
            subprocess.Popen(command[1:])
            response = "Proceso iniciado"

        elif command[0] == "STOP":
            pid = int(command[1])
            os.kill(pid, 9)
            response = "Proceso detenido"

        elif command[0] == "MONITOR":
            pid = int(command[1])
            proc = psutil.Process(pid)
            response = f"CPU: {proc.cpu_percent()}% MEM: {proc.memory_percent()}%"

        else:
            response = "Comando no válido"

        conn.send(response.encode())

    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Servidor escuchando en puerto 5000...")

while True:
    conn, addr = server.accept()
    thread = threading.Thread(target=handle_client, args=(conn, addr))
    thread.start()

