from functions.connect_rpc import connect_rpc

def server_files():
    server = connect_rpc().server
    return server.show_files()