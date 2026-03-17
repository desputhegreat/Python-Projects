# THIS PROJECT IS ONGOING
import socket
import threading

#initializing
addr = ("127.0.0.1", 5000)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(addr)
clients_list = []
server.listen()
print(f"Server successfully initialized on {addr[0]}:{addr[1]}")

#function to remove disconnected clients
def remove(client_socket):
    try:
        clients_list.remove(client_socket)
    except ValueError:
        pass
    finally:    
        client_socket.close()
        print("Someone disconnected"), broadcast("Someone disconnected", None)

#function to broadcast message to all clients
def broadcast(message, sender):
    print(sender, message)
    if message != '':
        for client in clients_list.copy(): 
            try: 
                if client != sender: client.send(message.encode())
            except ConnectionResetError: remove(client)    

# unction to receive message from a client socket and call broadcast()
def message_receiver(client_socket):
    try:    
        while True:
            message = client_socket.recv(1024)
            if not message:
                raise ConnectionResetError
            broadcast(message.decode(), client_socket)
    except ConnectionResetError:
        remove(client_socket)

# function to create threads for each user to connect
def create_thread():
    while True:
        client_socket, _ = server.accept()
        clients_list.append(client_socket)
        print("Someone joined")
        #add auth here
        thread = threading.Thread(target=message_receiver, args=(client_socket,))
        thread.start()

create_thread()        