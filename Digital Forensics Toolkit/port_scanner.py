# modules
import threading
import socket
import queue

# user input
server = input("Enter the IPV4/Domain Address to connect: ")
port_range = input("Enter the port range (x-y): ")
port_range = port_range.split("-")  # splits the port range into a list
ports = []  # ports will be stored in this

while True:
    try:
        # gets lower limit of port range
        min_range = min(int(port_range[0]), int(port_range[1]))
        # gets upper limit of port range
        max_range = max(int(port_range[0]), int(port_range[1]))+1

        if max_range > 65535 or min_range < 1:  # checks if port is in valid range
            raise ValueError

        # puts each port from the port_range into ports
        for port in range(min_range, max_range):
            ports.append(port)
        break

    except ValueError:  # error handeling for invalid values
        port_range = input("Invalid Port range. Please Try again (x-y): ")
        port_range = port_range.split("-")  # splits the port range into a list

ports_queue = queue.Queue()  # creates a queue

for port in ports:
    ports_queue.put(port) # puts the ports into the ports_queue one by one

# results will be stored in these
closed_ports = []  
open_ports = []
other_ports = []
timeout_ports = []
# target for each thread

def worker():
    # gets the port from ports_queue and calls connect function until the queue is empty
    while not ports_queue.empty():
        port = ports_queue.get()
        connect(port)

def connect(port):
    # creates a IPV4, TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)  # sets the timeout for the socket 1 seconds
    # tries to connect to the server and handles some errors accordingly
    try:
        sock.connect((server, port))
        open_ports.append(f"Port {port}: OPEN")
    except ConnectionError:
        closed_ports.append(f"Port {port}: CLOSED")
    except TimeoutError:
        timeout_ports.append(f"Port {port}: TIMEOUT")
    except Exception as e:
        other_ports.append(f"Port {port}: {e}")
    finally:
        sock.close()  # closes the socket
        ports_queue.task_done()  # marks the task done


# calculates the total number of threads to be created
thread_count = min(50, len(ports))

# creates the total number of threads based on thread count with target=worker and starts them
threads = [threading.Thread(target=worker) for _ in range(0,thread_count)]
for thread in threads: thread.start()

ports_queue.join()  # waits until each port is marked done

# prints the results
for port in open_ports: print(port)
for port in closed_ports: print(port)
for port in timeout_ports: print(port)
for port in other_ports: print(port)
print("Wallah I'm finished!")
