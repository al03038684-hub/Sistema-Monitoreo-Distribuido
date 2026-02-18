import socket
import threading

HOST = "localhost"
PORT = 5000          # Puerto donde escucha el middleware
SERVER_PORT = 6000   # Puerto donde está el servidor real

def handle_client(client_conn):

    # Conectarse al servidor real
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.connect((HOST, SERVER_PORT))

    while True:
        data = client_conn.recv(1024)
        if not data:
            break

        # Enviar al servidor
        server.send(data)

        # Recibir respuesta del servidor
        response = server.recv(1024)

        # Mandarla al cliente
        client_conn.send(response)

    client_conn.close()
    server.close()


middleware = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
middleware.bind((HOST, PORT))
middleware.listen()

print("Middleware escuchando en puerto 5000...")

while True:
    conn, addr = middleware.accept()
    print("Cliente conectado al middleware:", addr)

    thread = threading.Thread(target=handle_client, args=(conn,))
    thread.start()
