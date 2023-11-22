import xmlrpc.client

class connect_rpc:
    def __init__(self):
        self.server = xmlrpc.client.ServerProxy('http://is-rpc-server:9000')