import time
import random

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.leader_id = None
        self.nodes = set()

    def add_node(self, node):
        self.nodes.add(node)

    def start_election(self):
        print(f"Node {self.node_id} starts election")
        higher_nodes = [node for node in self.nodes if node.node_id > self.node_id]
        if not higher_nodes:
            self.declare_leader()
        else:
            for node in higher_nodes:
                if node.ping():
                    print(f"Node {node.node_id} responded, {self.node_id} failed")
                    return
            print(f"No higher nodes responded. Node {self.node_id} declares itself as leader")
            self.declare_leader()

    def ping(self):
        # Simulating node response (50% chance)
        return random.choice([True, False])

    def declare_leader(self):
        self.leader_id = self.node_id
        print(f"Node {self.node_id} is the new leader")

    def crash(self):
        # Simulating node failure
        print(f"Node {self.node_id} crashes")
        self.nodes.remove(self)

def simulate(nodes):
    print("Simulation starts\n")
    while True:
        time.sleep(2)
        leader = None
        for node in nodes:
            if node.leader_id is not None:
                leader = node
                break
        if leader is None:
            print("No leader detected. Initiating election process...")
            nodes.sort(key=lambda x: x.node_id, reverse=True)
            for node in nodes:
                node.start_election()
            print("Election process completed")
        else:
            print(f"Leader is Node {leader.leader_id}. Checking leader status...")
            if not leader.ping():
                print(f"Leader Node {leader.leader_id} is unresponsive. Initiating election process...")
                nodes.sort(key=lambda x: x.node_id, reverse=True)
                for node in nodes:
                    node.start_election()
                print("Election process completed")
            else:
                print("Leader is active. No action needed.\n")
        time.sleep(5)

if __name__ == "__main__":
    nodes = [Node(i) for i in range(1, 5)]  # Create nodes
    for i, node in enumerate(nodes):
        node.add_node(nodes[(i + 1) % len(nodes)])  # Connect each node to the next one in the list
    simulate(nodes)  # Start simulation
