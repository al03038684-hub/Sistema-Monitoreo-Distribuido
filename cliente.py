import socket

HOST = "localhost"  # mismo equipo
PORT = 5000         # mismo puerto del servidor

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((HOST, PORT))

print("Conectado al servidor")

mensaje = input("Escribe un mensaje para enviar al servidor: ")
cliente.send(mensaje.encode())

respuesta = cliente.recv(1024).decode()
print("Respuesta del servidor:", respuesta)

cliente.close()
