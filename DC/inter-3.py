from multiprocessing import Process, Queue
import os


def child_process(queue):
    message = "Hello from the child process! (PID: {})".format(os.getpid())
    queue.put(message)

if __name__ == '__main__':
    
    queue = Queue()

    
    child = Process(target=child_process, args=(queue,))

    
    child.start()

    
    child.join()

    
    message_from_child = queue.get()

    print("Message received from the child process:", message_from_child)
