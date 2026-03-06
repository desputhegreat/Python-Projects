#server
import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
adr = ("127.0.0.1", 5000)

server.bind(adr)
print("Waiting for connections...")
server.listen()
clients = []

def accepter():
    while True:    
        client_socket, client_addr = server.accept()
        clients.append(client_socket)
        print(f"{client_addr} joined")
        client_thread = threading.Thread(target=recv_brod, args=(client_socket,)) 
        client_thread.start()

def recv_brod(client_socket):
    while True:
        try:    
            msg = client_socket.recv(1024)
            if msg != b'':    
                broadcast(msg, client_socket)
                print(msg.decode())
        except ConnectionResetError:
            if client_socket in clients:
                clients.remove(client_socket)
            client_socket.close()
            break    

def broadcast(msg, sender):
    for client_socket in clients:
        if client_socket != sender:
            client_socket.send(msg)
            
accepter_thread = threading.Thread(target=accepter)

accepter_thread.start()

    