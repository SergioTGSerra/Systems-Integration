from functions.connect_rpc import connect_rpc

def delete_file_server(file_id):
    server = connect_rpc().server
    return server.delete_file(file_id)