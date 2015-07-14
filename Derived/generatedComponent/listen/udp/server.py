import SocketServer
import json
from datetime import datetime, date
import sys

class UDPHandler(SocketServer.BaseRequestHandler):

    def schedule(self, message):
        # print "Schedule for UDP not yet implemented. But supposed to write the request into requests"
        blocks = message.split("&")
        response = ""
        if len(blocks) < 2:
            return "Error: Too few arguments."
        else:
            stamp = "{:%Y%m%d%H%M%S%f}".format(datetime.now())
            data = {}
            data["stamp"] = stamp
            data["component"] = blocks[0]
            data["protocol"] = "UDP"
            data["status"] = "scheduled"
            data["message"] = {}
            data["message"]["head"] = blocks[1]
            data["message"]["data"] = {}
            for block in blocks[2:]:
                parts = block.split("#")
                if len(parts) != 2:
                    return "Error: Malformed request."
                data["message"]["data"][parts[0]] = parts[1]

            with open("../requests/"+stamp+".request", "w") as request_file: #Add ../ if testing from udp folder.
                request_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            return "Success: Request scheduled as ["+stamp+".request]"

    def process(self):
        response = self.schedule(self.data) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.socket.sendto(response+"\n", self.client_address)

    def handle(self):
        self.data = self.request[0].strip()
        self.socket = self.request[1]
        self.process()

if __name__ == "__main__":
    HOST, PORT = "localhost", 5020
    if len(sys.argv) == 3:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    server = SocketServer.UDPServer((HOST, PORT), UDPHandler)
    server.serve_forever()