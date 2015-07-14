import http.client, urllib.parse
import socket
import getpass
import sys
import telnetlib
import serial
import io
import smbus

class HTTP:
	def __init__(self, location, formats, model, endpoint, data):
		self.location = location
		self.headers = {"Content-type": formats[0],"Accept": formats[1]}
		self.model = model #GET,POST,PUT,UPDATE,...
		self.endpoint = endpoint
		self.data = data

	def process(self):
		if self.model == "GET":
			self.conn = http.client.HTTPConnection(self.location)
			self.conn.request(self.model, self.endpoint)
			return self.conn.getresponse()
		elif self.model == "POST":
			self.conn = http.client.HTTPConnection(self.location)
			self.params = urllib.parse.urlencode(self.data)
			self.conn.request(self.model, self.endpoint, self.params, self.headers)
			return self.conn.getresponse()
		else:
			print "Waiting for implementation of model: "+self.model+"."

class TCP:
	def __init__(self, ip, port, length, message):
		self.ip = ip
		self.port = port
		self.length = length #Buffer size
		self.message = message

	def process(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.s.connect((self.ip, self.port))
		self.s.send(self.message)
		self.data = s.recv(self.length)
		self.s.close()
		return self.data

class UDP:
	def __init__(self, ip, port, message):
		self.ip = ip
		self.port = port
		self.message = message

	def process(self):
		self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(self.message, (self.ip, self.port))
		return "Sent!"

class TELNET:
	def __init__(self, host, user, password=None, commands=None):#Commands is a list.
		self.host = host
		self.user = user
		self.password = password
		self.commands = commands

	def process(self):
		self.tn = telnetlib.Telnet(self.host)
		self.tn.write(self.user + "\n")
		if password:
			self.tn.read_until("Password: ")
    		self.tn.write(self.password + "\n")
    	for command in self.commands:
    		self.tn.write(command + "\n")
		return self.tn.read_all()

class SERIAL:
	def __init__(self, location, baudrate, timeout=1, data):
		self.location = location
		self.baudrate = baudrate
		self.timeout = timeout
		self.data = data

	def process(self):
		self.ser = serial.Serial(self.location, self.baudrate, self.timeout)
		if not ser.isOpen():
			self.ser.open()
		self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
		self.sio.write(unicode(self.data+"\n"))
		self.sio.flush()
		return self.sio.readline()

class I2C:
	def __init__(self, line, address, sleep=1, data=[]): #Data is binary data
		self.line = line
		self.address = address
		self.sleep = sleep
		self.data = data

	def process(self):
		self.bus = smbus.SMBus(self.line) 
		self.result = []
		for d in self.data:
			self.bus.write_byte(self.address, d)
			time.sleep(self.sleep)
			self.result += self.bus.read_byte(self.address)
		return self.result

class Client:
	def __init__(protocol, location, **kwargs):
		self.protocol = protocol
		self.location = location
		self.kwargs = kwargs

	def process(self):
		if self.protocol == "HTTP":
			httpClient = HTTP(self.location, self.kwargs)
			return httpClient.process()
		elif self.protocol == "TCP":
			tcpClient = TCP(self.location, self.kwargs)
			return tcpClient.process()
		elif self.protocol == "UDP":
			udpClient = UDP(self.location, self.kwargs)
			return udpClient.process()
		elif self.protocol == "TELNET":
			telnetClient = TELNET(self.location, self.kwargs)
			return telnetClient.process()
		elif self.protocol == "SERIAL":
			serialClient = SERIAL(self.location, self.kwargs)
			return serialClient.process()
		elif self.protocol == "I2C":
			i2cClient = I2C(self.location, self.kwargs)
			return i2cClient.process()
		else:
			print "Waiting for implementation of protocol: "+self.protocol+"."