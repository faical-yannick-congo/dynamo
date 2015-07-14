import SocketServer
import json
from datetime import datetime

class TCPHandler(SocketServer.BaseRequestHandler):

    def schedule(self, message):
        print "Schedule for TCP not yet implemented. But supposed to write the request into requests"

    def process(self):
        self.schedule(self.message) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.request.sendall("SCHEDULED")

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.message = self.request.recv(1024).strip()
        self.process()

if __name__ == "__main__":
    HOST, PORT = "localhost", 5010
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()