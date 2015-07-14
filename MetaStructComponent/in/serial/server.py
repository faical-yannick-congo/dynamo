import sys, os, serial, threading, io

class SERIALHandler:
    def __init__(self, serial):
        self.serial = serial
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))

    def shortcut(self):# Turn this into a thread. I should use this for the other servers too so that they do not lock the terminal running them.
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(1)
        self.thread_read.start()
        self.writer()

    def schedule(self, message):
        print "Schedule for Serial not yet implemented. But supposed to write the request into requests"

    def process(self):
        self.schedule(self.message) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.serial.write("SCHEDULED")
    
    def reader(self):  #The listener function called.
        while self.alive:
            try:
                self.message = self.sio.readline()#Data should be ordered in line. So at the end of json string add \n
                if self.message:
                    self.serial.write(unicode("SCHEDULED"))
                    sio.flush()
            except socket.error, msg:
                print msg
                #probably got disconnected
                break
        self.alive = False

    def stop(self):
        """Stop listening"""
        if self.alive:
            self.alive = False
            self.thread_read.join()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        LOCATION = sys.argv[1]
        try:
            BAUDRATE = int(sys.argv[2])
        except:
            print "Warning: Baudrate has to be an integer."
        try:
            TIMEOUT = int sys.argv[3]
        except:
            print "Warning: Timeout has to be an integer."
        try:
            ser = serial.Serial(LOCATION, BAUDRATE, TIMEOUT)
            if not ser.isOpen():
                ser.open()
            r = SERIALHandler(ser)
            r.shortcut()
        except serial.SerialException, e:
            print "Could not open serial port %s: %s" % (ser.portstr, e)
            sys.exit(1)
    else:
        print "Usage: python server.py location(/dev/tty874) baudrate(9600) timeout(10sec)"