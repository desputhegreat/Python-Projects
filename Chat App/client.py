#THIS PROJECT IS ONGOING
import socket
import threading
import queue
#initializing
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
addr = ("127.0.0.1", 5000)
try:
    server.connect(addr)
except ConnectionRefusedError:
    print("Can't connect to server")
    exit()
messages = queue.Queue

#function to send the messages to the server with error handling
def message_sender():
    try:    
        while True:
            if messages.empty(): 
                message = input("")
            else:
                print(messages.get())
                messages.task_done()
                message = input("")
            server.sendall(message.encode())
    except ConnectionResetError:
        print("Server Disconnected")
        exit()

# function to receive the incoming messeges from the server with error handling
def message_receiver():
    try:    
        while True:
            message = server.recv(1024).decode()
            # bug
            if message != '': messages.put(message)
    except ConnectionResetError:
        print("Server Disconnected")
        exit()


# creating and starting threads
reciever_thread = threading.Thread(target=message_receiver)
sender_thread = threading.Thread(target=message_sender)
reciever_thread.start(), sender_thread.start()