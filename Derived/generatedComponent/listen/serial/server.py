import sys, os, serial, threading, io
from datetime import datetime, date
import json

class SERIALHandler:
    def __init__(self, serial):
        self.serial = serial
        self.sio = io.TextIOWrapper(io.BufferedRWPair(self.serial, self.serial))

    def shortcut(self):# Turn this into a thread. I should use this for the other servers too so that they do not lock the terminal running them.
        self.alive = True
        self.thread_read = threading.Thread(target=self.reader)
        self.thread_read.setDaemon(1)
        self.thread_read.start()
        self.reader()

    def schedule(self, message):
        # print "Schedule for Serial not yet implemented. But supposed to write the request into requests"
        blocks = message.split("&")
        response = ""
        if len(blocks) < 2:
            return "Error: Too few arguments."
        else:
            stamp = "{:%Y%m%d%H%M%S%f}".format(datetime.now())
            data = {}
            data["stamp"] = stamp
            data["component"] = blocks[0]
            data["protocol"] = "SERIAL"
            data["status"] = "scheduled"
            data["message"] = {}
            data["message"]["head"] = blocks[1]
            data["message"]["data"] = {}
            for block in blocks[2:]:
                parts = block.split("#")
                if len(parts) != 2:
                    return "Error: Malformed request."
                data["message"]["data"][parts[0]] = parts[1].replace("\n","")

            with open("../requests/"+stamp+".request","w") as request_file: #Add ../ if testing from serial folder.
                request_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
            return "Success: Request scheduled as ["+stamp+".request]"

    def process(self):
        response = self.schedule(self.message) # Maybe use json.loads or json.dumps to give a json object or leave it as text.
        self.serial.write(response+"\n")
        self.sio.flush()
    
    def reader(self):  #The listener function called.
        while self.alive:
            try:
                self.message = self.sio.readline()#Data should be ordered in line. So at the end of json string add \n
                if self.message:
                    print "Received: "+self.message
                    # self.serial.write("SCHEDULED")
                    # sio.flush()
                    self.process()
            except serial.SerialException, e:
                print "Could not open serial port %s: %s" % (self.serial.portstr, e)
                #probably got disconnected
                break
        self.alive = False

    def stop(self):
        """Stop listening"""
        if self.alive:
            self.alive = False
            self.thread_read.join()

if __name__ == '__main__':
    if len(sys.argv) == 4:
        LOCATION = sys.argv[1]
        try:
            BAUDRATE = int(sys.argv[2])
        except:
            print "Warning: Baudrate has to be an integer."
        try:
            TIMEOUT = int(sys.argv[3])
        except:
            print "Warning: Timeout has to be an integer."
        try:
            ser = serial.Serial(LOCATION, BAUDRATE, timeout=TIMEOUT)
            if not ser.isOpen():
                ser.open()
            r = SERIALHandler(ser)
            r.shortcut()
        except serial.SerialException, e:
            print "Could not open serial port %s: %s" % (ser.portstr, e)
            sys.exit(1)
    else:
        print "Usage: python server.py location(/dev/tty874) baudrate(9600) timeout(10sec)"