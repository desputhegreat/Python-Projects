#client
import socket
import threading
import queue
from auth import auth_client

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
address = ("127.0.0.1", 5000)
sock.connect(address)
messages = queue.Queue()

user = input("Please enter your username: ")

def message_sender():
    while True:
        if not messages.empty():
            print(messages.get())
            messages.task_done()
        message = input(f"<{user}> ")
        message = f"<{user}> " + message
        sock.send(message.encode())

def message_reciever():
    while True:
        message = sock.recv(1024)
        if message != b'':
            messages.put(message.decode())
        else:
            print("Server Disconnected")
            exit()
auth_client(sock, user)

message_sender_thread = threading.Thread(target=message_sender)
message_reciever_thread = threading.Thread(target=message_reciever)
message_sender_thread.start()
message_reciever_thread.start()