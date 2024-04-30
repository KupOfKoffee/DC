class LoadBalancer:
    def __init__(self, servers):
        self.servers = servers
        self.current_index = 0

    def next_server(self):
        server = self.servers[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.servers)
        return server

# Example usage
servers = ["Server1", "Server2", "Server3"]
load_balancer = LoadBalancer(servers)

# Simulate incoming requests
for i in range(10):
    server = load_balancer.next_server()
    print(f"Request {i+1} routed to {server}")


'''This code defines a LoadBalancer class with a list of server names passed as an argument. 
The next_server() method returns the next server in the list according to the Round Robin algorithm.

Here's how the example works:

We create a list of server names.
We instantiate a LoadBalancer object with the list of server names.
We simulate 10 incoming requests by calling next_server() method each time and printing the 
server to which the request is routed.
This is a very basic implementation for demonstration purposes. In a real-world scenario, 
you may need to consider factors such as server health checks, server weights, and request/response processing times.'''