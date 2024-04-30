import threading
import time

class GroupCommunication:
    def __init__(self):
        self.messages = []
        self.lock = threading.Lock()
        self.terminate_flag = threading.Event()

    def send(self, message):
        with self.lock:
            self.messages.append(message)

    def receive(self):
        while not self.terminate_flag.is_set() or self.messages:
            with self.lock:
                if self.messages:
                    print("Received message:", self.messages.pop(0))
            time.sleep(1)

    def stop_receiver(self):
        self.terminate_flag.set()

def sender(group_comm):
    for i in range(5):
        group_comm.send(f"Message {i}")
        time.sleep(0.5)
    group_comm.stop_receiver()

def main():
    group_comm = GroupCommunication()
    receiver = threading.Thread(target=group_comm.receive)
    sender_thread = threading.Thread(target=sender, args=(group_comm,))

    receiver.start()
    sender_thread.start()

    sender_thread.join()
    receiver.join()
    print("Group communication completed.")

if __name__ == "__main__":
    main()
