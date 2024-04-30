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
token_lock = threading.Lock()
has_token = False
request_queue = []
reply_queue = [0] * N

def send_request():
    global has_token
    global request_queue
    global reply_queue
    global tid
    
    with request_lock:
        print(f"{now().strftime('%M:%S')} | [Process {tid}]: Sending request for critical section")
        request_queue.append(tid)
        for i in range(N):
            if i != tid:
                comm.send(('REQUEST', tid), dest=i)
    
    while True:
        all_replies_received = all(reply_queue)
        if all_replies_received:
            with token_lock:
                has_token = True
                print(f"{now().strftime('%M:%S')} | [Process {tid}]: Received all replies. Acquired token.")
                reply_queue = [0] * N
            break
        time.sleep(0.5)

def handle_request(message, source):
    global has_token
    global request_queue
    global reply_queue
    global tid
    
    req_id = message[1]
    
    if not has_token:
        print(f"{now().strftime('%M:%S')} | [Process {tid}]: Received request from Process {source}. Sending reply.")
        comm.send(('REPLY', tid), dest=source)
    else:
        reply_queue[source] = 1
        print(f"{now().strftime('%M:%S')} | [Process {tid}]: Received request from Process {source}. Already have token. Queuing reply.")
        if min(request_queue) == tid:
            send_reply_to_min()

def send_reply_to_min():
    global request_queue
    global reply_queue
    global tid
    
    min_id = min(request_queue)
    min_index = request_queue.index(min_id)
    
    with token_lock:
        request_queue.pop(min_index)
        reply_queue = [0] * N
        comm.send(('REPLY', tid), dest=min_id)
        print(f"{now().strftime('%M:%S')} | [Process {tid}]: Sent reply to Process {min_id}.")
        time.sleep(0.5)

def critical_section():
    global tid
    print(f"{now().strftime('%M:%S')} | [Process {tid}]: Entering critical section.")
    time.sleep(random.uniform(1, 3))
    print(f"{now().strftime('%M:%S')} | [Process {tid}]: Exiting critical section.")

def receive():
    global has_token
    global tid
    
    while True:
        message = comm.recv(source=MPI.ANY_SOURCE)
        if message[0] == 'REQUEST':
            handle_request(message, message[1])
        elif message[0] == 'REPLY':
            print(f"{now().strftime('%M:%S')} | [Process {tid}]: Received reply from Process {message[1]}.")
            reply_queue[message[1]] = 1

# Start a thread to handle receiving messages
listener = threading.Thread(target=receive)
listener.start()

if tid == 0:
    has_token = True
    print(f"{now().strftime('%M:%S')} | [Process {tid}]: Initialized with token.")
else:
    send_request()

while True:
    if has_token:
        critical_section()
        has_token = False
        send_request()
    time.sleep(random.uniform(1, 3))
