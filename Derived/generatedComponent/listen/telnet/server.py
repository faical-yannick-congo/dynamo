from gevent import monkey; monkey.patch_all()
import gevent.server
from telnetsrv.paramiko_ssh import SSHHandler, getRsaKeyFile
from telnetsrv.green import TelnetHandler, command
from datetime import datetime, date
import sys, json
import logging

SSHON = False

class MyTelnetHandler(TelnetHandler):
    WELCOME = "Welcome to the DynamicDerivation telnet input."

    def schedule(self, message):
        #print "Schedule for Telnet not yet implemented. But supposed to write the request into requests"
        blocks = message[0].split("&")
        response = ""
        if len(blocks) < 2:
            return "Error: Too few arguments."
        else:
            stamp = "{:%Y%m%d%H%M%S%f}".format(datetime.now())
            data = {}
            data["stamp"] = stamp
            data["component"] = blocks[0]
            if not SSHON:
                data["protocol"] = "TELNET"
            else:
                data["protocol"] = "SSH"
            data["status"] = "scheduled"
            data["message"] = {}
            data["message"]["head"] = blocks[1]
            data["message"]["data"] = {}
            for block in blocks[2:]:
                parts = block.split("#")
                if len(parts) != 2:
                    return "Error: Malformed request."
                data["message"]["data"][parts[0]] = parts[1]

            with open("../requests/"+stamp+".request","w") as request_file: #Add ../ if testing from telnet folder.
                request_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            return "Success: Request scheduled as ["+stamp+".request]"

    def process(self, params):
        response = self.schedule(params) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.writeresponse(response)

    @command(['communicate'])
    def command_communicate(self, params):
        self.process(params)

class MySSHHandler(SSHHandler):
    # Set the unique host key
    host_key = getRsaKeyFile('server_fingerprint.key')

    # Instruct this SSH handler to use MyTelnetHandler for any PTY connections
    telnet_handler = MyTelnetHandler

    # def authCallbackUsername(self, username):
    #     # These users do not require a password
    #     if username not in ['john', 'eric', 'terry', 'graham']:
    #        raise RuntimeError('Not a Python!')

    def authCallback(self, username, password):
        # Super secret password:
        if username != 'root' and password != 'admin':
           raise RuntimeError('Wrong password!')

if __name__ == "__main__":
    i=0
    HOST, PORT = "localhost", 5020
    SSH=5022
    for command in sys.argv:
        if command == "--host":
            HOST=sys.argv[i+1]
        elif command == "--port":
            PORT=int(sys.argv[i+1])
        elif command == "--ssh":
            SSHON=True
            SSH=int(sys.argv[i+1])
        i+=1
    if SSHON:
        print "SSH ON!"
        sshserver = gevent.server.StreamServer((HOST, SSH), MySSHHandler.streamserver_handle)
        logging.basicConfig()
        sshserver.serve_forever()
    else:
        print "SSH OFF!"
        telnetserver = gevent.server.StreamServer((HOST, PORT), MyTelnetHandler.streamserver_handle)
        telnetserver.serve_forever()