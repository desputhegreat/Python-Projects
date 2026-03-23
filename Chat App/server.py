# THIS PROJECT IS ONGOING
import socket
import threading
from auth import server_auth
import json

# initializing
addr = ("127.0.0.1", 5000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
clients_list = []
server.listen()
print(f"Server successfully initialized on {addr[0]}:{addr[1]}")
database = {}
# function to remove disconnected clients


def remove(client_socket):
    try:
        clients_list.remove(client_socket)
    except ValueError:
        pass
    finally:
        client_socket.close()
        print("Someone disconnected"), broadcast("Someone disconnected", None)

# function to broadcast message to all clients


def broadcast(message, sender):
    print(sender, message)
    if message != '':
        for client in clients_list.copy():
            try:
                if client != sender:
                    client.send(message.encode())
            except ConnectionResetError:
                remove(client)

# function to receive message from a client socket and call broadcast()


def message_receiver(client_socket):
    try:
        while True:
            message = client_socket.recv(1024)
            if not message:
                raise ConnectionResetError
            broadcast(message.decode(), client_socket)
    except ConnectionResetError:
        remove(client_socket)

# function to load/save database


def update_database(x):
    global database
    if x == "loading":
        with open("C:/VsCode/Utils/Chat App/data/database.json", "r") as file:
            database = json.load(file)
    else:
        with open("C:/VsCode/Utils/Chat App/data/database.json", "w") as file:
            json.dump(database, file, indent=4)

# function to create threads for each user to connect


def create_thread():
    while True:
        client_socket, _ = server.accept()
        clients_list.append(client_socket)
        update_database("loading")
        server_auth(client_socket, database)
        update_database("saving")
        print("Someone joined")
        thread = threading.Thread(
            target=message_receiver, args=(client_socket,))
        thread.start()


create_thread()
