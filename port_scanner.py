#modules
import threading
import socket
import queue

#user input
server = input("Enter the IPV4/Domain Address to connect: ") 
port_range = input("Enter the port range (x-y): ") 

port_range = port_range.split("-") #splits the port range into a list

ports = [] #ports will be stored in this

#puts each port from the port range into ports
for port in range(int(port_range[0]), int(port_range[1]) + 1):
    ports.append(port)                                        

ports_queue = queue.Queue() #creates a queue

for port in ports:   
    ports_queue.put(port)   #puts the ports into the ports_queue one by one

results = [] #results will be stored in this

#target for each thread
def worker():
    #gets the port from ports_queue and creates a IPV4, TCP socket until the queue is empty 
    while not ports_queue.empty():
        port = ports_queue.get()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) #sets the timeout for the socket 1 seconds
        #tries to connect to the server and handles some errors accordingly
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
            sock.close() #closes the socket 
        
        ports_queue.task_done() #marks the task done

thread_count = min(50, len(ports)) #calculates the total number of threads to be created                      

#creates the total number of threads based on thread count with target=worker and starts them
for _ in range(0, thread_count):
    thread = threading.Thread(target=worker)
    thread.start()  

ports_queue.join() #waits until each port is marked done

#prints the results
for result in results:
    print(result)

print("Wallah I'm finished!")