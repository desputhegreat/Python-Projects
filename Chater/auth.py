import socket
import hashlib
import json

def auth_client(sock, user):
    while True:    
        sock.send(user.encode())
        responce = sock.recv(1024).decode()
        if responce == "Login":
            password = input("Enter your password: ")
            sock.send(password.encode())
            responce = sock.recv(1024).decode()
            if responce == "Logged in":
                print("Successfully Logged in!")
                break
            elif responce == "Incorrect":
                while responce != "Correct":    
                    password = input("Incorrect Password. Try again: ")
                    sock.send(password.encode())
                    responce = sock.recv(1024).decode()
                break    
            else:
                print("Something went wrong")
                exit()    
        elif responce == "Register":
            password = input("Enter a strong password: ")
            sock.send(password.encode())
            print("Successfully Registered!")
            break
        else:
            print("Something went wrong")     
            exit()

def auth_server(client_socket, users, json_dir):
    while True:    
        user = client_socket.recv(1024).decode()
        if user in users:
            message = "Login"
            client_socket.send(message.encode())
            password = client_socket.recv(1024)
            if hashlib.sha256(password).hexdigest() == users[user]:
                message = "Logged in"
                client_socket.send(message.encode())
                break
            else:
                message = "Incorrect"
                client_socket.send(message.encode())
                while hashlib.sha256(password).hexdigest() != users[user]:
                    client_socket.send(message := "Nope".encode())   
                    password = client_socket.recv(1024)
                client_socket.send(message := "Correct".encode())
                break    
        else:
            message = "Register"
            client_socket.send(message.encode()) 
            password = client_socket.recv(1024)
            users[user] = hashlib.sha256(password).hexdigest()
            with open(json_dir, "w") as file:
                json.dump(users, file, indent=4)
            break
        