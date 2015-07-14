import SocketServer
import json
from datetime import datetime

class UDPHandler(SocketServer.BaseRequestHandler):

    def schedule(self, message):
        print "Schedule for UDP not yet implemented. But supposed to write the request into requests"

    def process(self):
        self.schedule(self.data) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.socket.sendto("SCHEDULED", self.client_address)

    def handle(self):
        self.data = self.request[0].strip()
        self.socket = self.request[1]
        self.process()

if __name__ == "__main__":
    HOST, PORT = "localhost", 5020
    server = SocketServer.UDPServer((HOST, PORT), UDPHandler)
    server.serve_forever()