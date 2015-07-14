import SocketServer
import json
from datetime import datetime, date
import sys


class TCPHandler(SocketServer.BaseRequestHandler):

    def schedule(self, message):
        #print "Schedule for TCP not yet implemented. But supposed to write the request into requests"
        blocks = message.split("&")
        if len(blocks) < 2:
            return "Error: Too few arguments."
        else:
            stamp = "{:%Y%m%d%H%M%S%f}".format(datetime.now())
            data = {}
            data["stamp"] = stamp
            data["component"] = blocks[0]
            data["protocol"] = "TCP"
            data["status"] = "scheduled"
            data["message"] = {}
            data["message"]["head"] = blocks[1]
            data["message"]["data"] = {}
            for block in blocks[2:]:
                parts = block.split("#")
                if len(parts) != 2:
                    return "Error: Malformed request."
                data["message"]["data"][parts[0]] = parts[1]

            with open("../requests/"+stamp+".request","w") as request_file: #Add ../ if testing from tcp folder.
                request_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            return "Success: Request scheduled as ["+stamp+".request]"
            

    def process(self):
        response = self.schedule(self.message) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.request.sendall(response+"\n")

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.message = self.request.recv(1024).strip()
        self.process()

if __name__ == "__main__":
    HOST, PORT = "localhost", 5010
    if len(sys.argv) == 3:
        HOST, PORT = sys.argv[1], int(sys.argv[2])
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
    server.serve_forever()