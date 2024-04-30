import xmlrpc.client

# Create an XML-RPC client
client = xmlrpc.client.ServerProxy("http://localhost:8000/")

# Call the remote function
result = client.add(5, 3)
print("Result from server:", result)
