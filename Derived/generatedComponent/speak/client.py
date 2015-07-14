import httplib, urllib
import socket
import getpass
import sys
import telnetlib
import serial
import io
#import smbus
#No I2C on my computer.

class HTTP:
	def __init__(self, location, formats=['application/json', 'application/json'], model="POST", endpoint=""):
		self.location = location
		self.headers = {"Content-type": formats[0],"Accept": formats[1]}
		self.model = model #GET,POST,PUT,UPDATE,...
		self.endpoint = endpoint

	def process(self, data):
		self.data = data
		try:
			if self.model == "GET":
				self.conn = httplib.HTTPConnection(self.location)
				self.conn.request(self.model, self.endpoint)
				return self.conn.getresponse()
			elif self.model == "POST":
				self.conn = httplib.HTTPConnection(self.location)
				self.params = urllib.urlencode({'response':self.data})
				self.conn.request(self.model, self.endpoint, self.params, self.headers)
				return self.conn.getresponse()
			else:
				print "Waiting for implementation of model: "+self.model+"."
		except:
			return "Failed to communicate with the component."

class TCP:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

	def process(self, message):
		self.message = message
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.s.connect((self.ip, self.port))
			self.s.send(self.message)
			self.data = s.recv(len(self.message))
			self.s.close()
			return self.data
		except:
			return "Failed to communicate with the component."

class UDP:
	def __init__(self, ip, port):
		self.ip = ip
		self.port = port

	def process(self, message):
		self.message = message
		try:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.sendto(self.message, (self.ip, self.port))
			return "Sent!"
		except:
			return "Failed to communicate with the component."

class TELNET:
	def __init__(self, host, port, command=None):#Commands is a list.
		self.host = host
		self.port = port
		self.password = password
		self.command = command

	def process(self, message):
		self.message = message
		try:
			self.tn = telnetlib.Telnet(self.host, self.port)
			self.tn.write(self.user + "\n")
			if password:
				self.tn.read_until("Password: ")
	    		self.tn.write(self.password + "\n")
	  		if command != None:
	  			self.tn.write(self.command + " " + self.message + "\n")
	  		else:
	  			self.tn.write(self.message + "\n")
			return self.tn.read_all()
		except:
			return "Failed to communicate with the component."



class SERIAL:
	def __init__(self, location, baudrate, timeout=1):
		self.location = location
		self.baudrate = baudrate
		self.timeout = timeout

	def process(self, data):
		self.data = data
		try:
			self.ser = serial.Serial(self.location, self.baudrate, self.timeout)
			if not ser.isOpen():
				self.ser.open()
			self.sio = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser))
			self.sio.write(unicode(self.data+"\n"))
			self.sio.flush()
			return self.sio.readline()
		except:
			return "Failed to communicate with the component."

# class I2C:
# 	def __init__(self, line, address, sleep=1): #Data is binary data
# 		self.line = line
# 		self.address = address
# 		self.sleep = sleep

# 	def process(self, data=[]):
# 		self.data = data
# 		try:
# 			self.bus = smbus.SMBus(self.line) 
# 			self.result = []
# 			for d in self.data:
# 				self.bus.write_byte(self.address, d)
# 				time.sleep(self.sleep)
# 				self.result += self.bus.read_byte(self.address)
# 			return self.result
# 		except:
# 			return "Failed to communicate with the component."

class Client:
	def __init__(protocol, location, **kwargs):
		self.protocol = protocol
		self.location = location
		self.kwargs = kwargs

	def process(self, data):
		if self.protocol == "HTTP":
			httpClient = HTTP(self.location, self.kwargs)
			return httpClient.process(data)
		elif self.protocol == "TCP":
			tcpClient = TCP(self.location, self.kwargs)
			return tcpClient.process(data)
		elif self.protocol == "UDP":
			udpClient = UDP(self.location, self.kwargs)
			return udpClient.process(data)
		elif self.protocol == "TELNET":
			telnetClient = TELNET(self.location, self.kwargs)
			return telnetClient.process(data)
		elif self.protocol == "SERIAL":
			serialClient = SERIAL(self.location, self.kwargs)
			return serialClient.process(data)
		elif self.protocol == "I2C":
			i2cClient = I2C(self.location, self.kwargs)
			return i2cClient.process(data)
		else:
			print "Waiting for implementation of protocol: "+self.protocol+"."