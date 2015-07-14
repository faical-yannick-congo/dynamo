from gevent import monkey; monkey.patch_all()
import gevent.server
from telnetsrv.paramiko_ssh import SSHHandler, getRsaKeyFile
from telnetsrv.green import TelnetHandler, command

class MyTelnetHandler(TelnetHandler):
    WELCOME = "Welcome to the DynamicDerivation telenet input."

    def schedule(self, message):
        print "Schedule for Telnet not yet implemented. But supposed to write the request into requests"

    def process(self, command, params):
        self.schedule([command, params]) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.writeresponse("SCHEDULED")

    @command(['sleep', 'destroy', 'update', 'wake', 'custom'])
    def command_echo(self, params):
        self.process(self, command, params)

class MySSHHandler(SSHHandler):
    # Set the unique host key
    host_key = getRsaKeyFile('server_fingerprint.key')

    # Instruct this SSH handler to use MyTelnetHandler for any PTY connections
    telnet_handler = MyTelnetHandler

    def authCallbackUsername(self, username):
        # These users do not require a password
        if username not in ['john', 'eric', 'terry', 'graham']:
           raise RuntimeError('Not a Python!')

    def authCallback(self, username, password):
        # Super secret password:
        if password != 'concord':
           raise RuntimeError('Wrong password!')

if __name__ == "__main__":
    i=0
    HOST, PORT = "localhost", 5020
    SSHON = False
    SSH=5022
    for command in argv:
        if command == "--host":
            HOST=argv[i+1]
        elif command == "--port":
            PORT=argv[i+1]
        elif command == "--ssh":
            SSHON=True
            SSH=argv[i+1]
        i++

    telnetserver = gevent.server.StreamServer((HOST, PORT), MyTelnetHandler.streamserver_handle)
    telnetserver.start()
    if SSHON:
        sshserver = gevent.server.StreamServer(("", SSH), MySSHHandler.streamserver_handle)
        sshserver.serve_forever()