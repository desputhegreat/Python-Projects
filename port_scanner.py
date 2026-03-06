import threading
import socket
import queue

server = input("Enter the IPV4/Domain Address to connect: ")
ports = input("Enter the ports, seperated by a comma. No spaces.: ")
ports = ports.split(",")

ports_queue = queue.Queue()

for port in ports:
    ports_queue.put(port)
results = []
def worker():
    while not ports_queue.empty():
        port = ports_queue.get()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        try:
            sock.connect((server, int(port)))
            results.append(f"Port {port}: OPEN")
        except ConnectionError:
            results.append(f"Port {port}: CLOSED")
        except TimeoutError:
            results.append(f"Port {port}: TIMEOUT")    
        except Exception as e:
            results.append(f"Port {port}: {e}")
        finally:
            sock.close()
        ports_queue.task_done()

thread_count = min(50, len(ports))                       
threads = []

for _ in range(0, thread_count):
    thread = threading.Thread(target=worker)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
for i in results:
    print(i)
print("Wallah I'm finished!")