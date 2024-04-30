import time

class BerkeleyClockSync:
    def __init__(self, nodes):
        self.nodes = nodes

    def sync_clocks(self):
        master_time = self.get_master_time()
        for node in self.nodes:
            node.adjust_time(master_time)

    def get_master_time(self):
        return time.time()  # This could be replaced with a function to fetch time from a master node

class Node:
    def __init__(self, name, time_offset=0):
        self.name = name
        self.time_offset = time_offset

    def adjust_time(self, master_time):
        local_time = time.time() + self.time_offset
        adjustment = master_time - local_time
        self.time_offset += adjustment
        print(f"Node {self.name}: Adjusted time by {adjustment} seconds to {time.time() + self.time_offset}")

# Example usage
nodes = [
    Node("A", time_offset=5),
    Node("B", time_offset=-3),
    Node("C", time_offset=2)
]

berkeley_sync = BerkeleyClockSync(nodes)
berkeley_sync.sync_clocks()

'''BerkeleyClockSync class:
__init__: Initializes the BerkeleyClockSync object with a list of nodes.
sync_clocks: Synchronizes the clocks of all nodes by getting the master time and adjusting the time offsets of each node accordingly.
get_master_time: Gets the master time, which could be the current system time or fetched from a master node.
Node class:
__init__: Initializes a Node object with a name and an optional time offset.
adjust_time: Adjusts the time offset of the node to synchronize it with the master time.
Example usage:
Creates a list of nodes with different time offsets.
Creates an instance of BerkeleyClockSync with the list of nodes.
Calls sync_clocks to synchronize the clocks of all nodes.'''