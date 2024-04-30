import random
import sys
import threading
import time
import datetime
from mpi4py import MPI

now = datetime.datetime.now
comm = MPI.COMM_WORLD
tid = comm.Get_rank()
N = comm.Get_size()

request_lock = threading.Lock()
reply_lock = threading.Lock()
request_queue = []
replies_needed = 0
reply_received = [False] * N

def send_request():
    global request_queue
    global tid
    global replies_needed
    
    with request_lock:
        print(f"{now().strftime('%M:%S')} | [Process {tid}]: Sending request for critical section")
        request_queue.append(tid)
        replies_needed = N - 1
        for i in range(N):
            if i != tid:
                comm.send(('REQUEST', tid), dest=i)

def handle_request(message, source):
    global tid
    global request_queue
    
    req_id = message[1]
    
    if not request_queue or (req_id, source) < (request_queue[0], tid):
        with reply_lock:
            comm.send(('REPLY', tid), dest=source)
            print(f"{now().strftime('%M:%S')} | [Process {tid}]: Sent reply to Process {source}.")
    else:
        print(f"{now().strftime('%M:%S')} | [Process {tid}]: Queueing request from Process {source}.")
        request_queue.append(req_id)

def handle_reply(message, source):
    global tid
    global replies_needed
    global reply_received
    
    print(f"{now().strftime('%M:%S')} | [Process {tid}]: Received reply from Process {source}.")
    with reply_lock:
        replies_needed -= 1
        reply_received[source] = True

def critical_section():
    global tid
    
    print(f"{now().strftime('%M:%S')} | [Process {tid}]: Entering critical section.")
    time.sleep(random.uniform(1, 3))
    print(f"{now().strftime('%M:%S')} | [Process {tid}]: Exiting critical section.")

def receive():
    global tid
    
    while True:
        message = comm.recv(source=MPI.ANY_SOURCE)
        if message[0] == 'REQUEST':
            handle_request(message, message[1])
        elif message[0] == 'REPLY':
            handle_reply(message, message[1])

# Start a thread to handle receiving messages
listener = threading.Thread(target=receive)
listener.start()

while True:
    send_request()
    while replies_needed > 0:
        time.sleep(0.5)
    critical_section()
    request_queue = []
    reply_received = [False] * N
