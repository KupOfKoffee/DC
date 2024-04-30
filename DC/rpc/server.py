from xmlrpc.server import SimpleXMLRPCServer

# Define the function to be remotely called
def add(x, y):
    return x + y

# Create an XML-RPC server
server = SimpleXMLRPCServer(("localhost", 8000))
print("RPC server is listening on port 8000...")

# Register the function to be remotely accessible
server.register_function(add, "add")

# Start the server
server.serve_forever()
