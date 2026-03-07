#server
import socket
import threading
from auth import auth_server
import json

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("127.0.0.1", 5000)

server.bind(address)

print("Waiting for connections...")
server.listen()
clients = []

json_dir = "data/users.json"

with open(json_dir, "r") as file:
    users = json.load(file)

def accepter():
    while True:    
        client_socket, _ = server.accept()
        clients.append(client_socket)
        auth_server(client_socket, users, json_dir)

def reciver(client):
    while True:
        try:    
            msg = client.recv(1024)
            if msg != b'':    
                broadcaster(msg, client)
                print(msg.decode())
        except ConnectionResetError:
            if client in clients:
                clients.remove(client)
            client.close()
            break    

def broadcaster(msg, sender):
    for client in clients:
        if client != sender:
            client.send(msg)

accepter_thread = threading.Thread(target=accepter)
accepter_thread.start()

    