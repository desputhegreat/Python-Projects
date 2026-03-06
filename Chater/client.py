#client
import socket
import threading

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(("127.0.0.1", 5000))

def msg_sender():
    while True:
        message = input("> ")
        sock.send(message.encode())
def msg_reciever():
    while True:
        msg = sock.recv(1024)
        print(msg.decode())

msg_sender_thread = threading.Thread(target=msg_sender)
msg_reciever_thread = threading.Thread(target=msg_reciever)
msg_sender_thread.start()