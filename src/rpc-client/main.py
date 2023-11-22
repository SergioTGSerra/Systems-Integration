import xmlrpc.client

print("connecting to server...")
server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')

with open('/data/Global_Superstore2.csv', 'rb') as handle:
    binary_data = xmlrpc.client.Binary(handle.read())
    server.send_file(binary_data)