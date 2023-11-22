import xmlrpc.client
from functions.connect_rpc import connect_rpc

def send_file(file_name):
    if file_name.endswith('.csv'):
        with open(f'/data/{file_name}', 'rb') as handle:
            binary_data = xmlrpc.client.Binary(handle.read())
            server = connect_rpc().server
            return server.send_file(binary_data, file_name)
    else:
        return "Invalid file format. Only CSV files are supported."