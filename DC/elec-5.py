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
        elif all(not node.ping() for node in higher_nodes):
            print(f"No higher nodes responded. Node {self.node_id} declares itself as leader")
            self.declare_leader()

    def ping(self):
        return random.choice([True, False])

    def declare_leader(self):
        self.leader_id = self.node_id
        print(f"Node {self.node_id} is the new leader")

def simulate(nodes, rounds):
    print("Simulation starts\n")
    for _ in range(rounds):
        time.sleep(2)
        leader = next((node for node in nodes if node.leader_id is not None), None)
        if leader is None or not leader.ping():
            print("Initiating election process...")
            nodes.sort(key=lambda x: x.node_id, reverse=True)
            for node in nodes:
                node.start_election()
            print("Election process completed")
        else:
            print(f"Leader is Node {leader.leader_id}. Checking leader status...")
        time.sleep(5)

if __name__ == "__main__":
    nodes = [Node(i) for i in range(1, 5)]  
    for i, node in enumerate(nodes):
        node.add_node(nodes[(i + 1) % len(nodes)])  
    simulate(nodes, 5)  # Running the simulation for 5 rounds
