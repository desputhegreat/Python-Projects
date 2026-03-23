import socket
import hashlib

def server_auth(client_socket, database):
    while True:
        user_name =  client_socket.recv(1024).decode()
        if user_name in database:
            client_socket.send("exists".encode())
            password = client_socket.recv(1024)
            password_hash = hashlib.sha256(password).hexdigest()
            if password_hash == database[user_name]:
                client_socket.send("success".encode())
                break
            else:
                while True:
                    client_socket.send("failed".encode())
                    password = client_socket.recv(1024)
                    password_hash = hashlib.sha256(password).hexdigest()
                    if password_hash == database[user_name]:
                        client_socket.send("success".encode())
                        break
                    else:
                        client_socket.send("failed".encode())
                break        
        else:
            client_socket.send("new".encode())
            password = client_socket.recv(1024)
            password_hash = hashlib.sha256(password).hexdigest()
            database[user_name] = password_hash
            break

def client_auth(server_socket):
    user_name = input("Enter your username: ")
    server_socket.send(user_name.encode())
    while True:    
        responce = server_socket.recv(1024)
        if responce.decode() == "exists":
            password = input("Enter your password: ")
            server_socket.send(password.encode())
            while True:
                responce = server_socket.recv(1024)
                if responce.decode() == "success":
                    print("Successfully Logged-In!")
                    break
                else:
                    password = input("Password Incorrect. Please Try Again: ")
                    server_socket.send(password.encode())
            break
        else:
            password = input("Enter a Strong Password: ")
            server_socket.send(password.encode())
            print("Successfully Registered")
            break