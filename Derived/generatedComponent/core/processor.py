import datetime
from speak import client
import subprocess


HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'
BOLD = '\033[1m'
UNDERLINE = '\033[4m'

class Processor:
	def __init__(self, stamp, logger, request, status, actions):
		self.stamp = stamp
		self.logger = logger
		self.request = request
		self.status = status
		self.actions = actions
		self.calibrate(self.request)
		self.client = None

	def log(self, trace, level=0):
		if level == 9999:
			print FAIL+BOLD+"\n\n[GeneratedComponent] "+UNDERLINE+WARNING+str(datetime.datetime.now())+ENDC+OKGREEN+" ---"+" Component loading..."+ENDC
			log_file = open(self.logger, 'a')
			log_file.write("\n\n[GeneratedComponent] "+str(datetime.datetime.now())+" --- Component loading...")
			log_file.close()
		else:
			print FAIL+BOLD+"[GeneratedComponent] "+UNDERLINE+WARNING+str(datetime.datetime.now())+ENDC+OKGREEN+" --- " + trace+ENDC
		if level == 0:
			log_file = open(self.logger, 'a')
			log_file.write("\n[GeneratedComponent] "+str(datetime.datetime.now())+" --- " + trace)
			log_file.close()

	def isSupported(self, protocol):
		for capability in self.status['capability']['capabilities']:
			if capability['protocol'] == protocol:
				return True
		return False

	
	def calibrate(self, request):
		#Think more here.
		#We have to find the component, check that it allows me to talk to it in its capabilities before instantiating the client.
		#There is a need for a priority in the protocol classification.
		protocol = request['protocol']
		if protocol == "SERIAL":
			if not self.isSupported('SERIAL'):
				self.log("Error: The requested (Serial) protocol is not in this component capabilities. Please fix this.")
			else:
				senderCapability = {}
				for capabil in self.status['mapping']['distribution']:
					if capabil['component'] == request['component']:
						senderCapability = capabil
						break
				#We will suppose here that a sender capability should contain the protocol it has.
				if len(senderCapability) == 0:
					self.log("Error: The communicating component is not mapped in my knowledge.")
				else:
					config = {}
					for proto in capabil['capabilities']:
						if proto['protocol'] == "SERIAL":
							config = proto
							break
					if len(config) == 0:
						# print "Error: The requested protocol is not mapped. We cannot respond to the sender."
						self.log("Error: The requested protocol is not mapped. We cannot respond to the sender.")
					else:	
						self.client = client.SERIAL(config['location'], config['baud'], config['timeout'])
						self.log("Serial protocol calibrated for the response.")
		elif protocol == "TCP":
			if not self.isSupported('TCP'):
				self.log("Error: The requested (Tcp) protocol is not in this component capabilities. Please fix this.")
			else:
				senderCapability = {}
				for capabil in self.status['mapping']['distribution']:
					if capabil['component'] == request['component']:
						senderCapability = capabil
						break
				#We will suppose here that a sender capability should contain the protocol it has.
				if len(senderCapability) == 0:
					self.log("Error: The communicating component is not mapped in my knowledge.")
				else:
					config = {}
					for proto in capabil['capabilities']:
						if proto['protocol'] == "TCP":
							config = proto
							break
					if len(config) == 0:
						# print "Error: The requested protocol is not mapped. We cannot respond to the sender."
						self.log("Error: The requested protocol is not mapped. We cannot respond to the sender.")
					else:	
						self.client = client.TCP(config['host'], config['port'])
						self.log("Tcp protocol calibrated for the response.")
		elif protocol == "UDP":
			if not self.isSupported('UDP'):
				self.log("Error: The requested (Udp) protocol is not in this component capabilities. Please fix this.")
			else:
				senderCapability = {}
				for capabil in self.status['mapping']['distribution']:
					if capabil['component'] == request['component']:
						senderCapability = capabil
						break
				#We will suppose here that a sender capability should contain the protocol it has.
				if len(senderCapability) == 0:
					self.log("Error: The communicating component is not mapped in my knowledge.")
				else:
					config = {}
					for proto in capabil['capabilities']:
						if proto['protocol'] == "UDP":
							config = proto
							break
					if len(config) == 0:
						# print "Error: The requested protocol is not mapped. We cannot respond to the sender."
						self.log("Error: The requested protocol is not mapped. We cannot respond to the sender.")
					else:	
						self.client = client.UDP(config['host'], config['port'])
						self.log("Udp protocol calibrated for the response.")
		elif protocol == "TELNET":
			if not self.isSupported('SERIAL'):
				self.log("Error: The requested (Telnet) protocol is not in this component capabilities. Please fix this.")
			else:
				senderCapability = {}
				for capabil in self.status['mapping']['distribution']:
					if capabil['component'] == request['component']:
						senderCapability = capabil
						break
				if len(senderCapability) == 0:
					self.log("Error: The communicating component is not mapped in my knowledge.")
				else:
					#We will suppose here that a sender capability should contain the protocol it has.
					config = {}
					for proto in capabil['capabilities']:
						if proto['protocol'] == "TELNET":
							config = proto
							break
					if len(config) == 0:
						# print "Error: The requested protocol is not mapped. We cannot respond to the sender."
						self.log("Error: The requested protocol is not mapped. We cannot respond to the sender.")
					else:	
						self.client = client.TELNET(config['host'], config['port'], config['command'])
						self.log("Telnet protocol calibrated for the response.")
		elif protocol == "SSH":
			if not self.isSupported('SSH'):
				self.log("Error: The requested (Ssh) protocol is not in this component capabilities. Please fix this.")
			else:
				senderCapability = {}
				for capabil in self.status['mapping']['distribution']:
					if capabil['component'] == request['component']:
						senderCapability = capabil
						break
				if len(senderCapability) == 0:
					self.log("Error: The communicating component is not mapped in my knowledge.")
				else:
					#We will suppose here that a sender capability should contain the protocol it has.
					config = {}
					for proto in capabil['capabilities']:
						if proto['protocol'] == "SSH":
							config = proto
							break
					if len(config) == 0:
						# print "Error: The requested protocol is not mapped. We cannot respond to the sender."
						self.log("Error: The requested protocol is not mapped. We cannot respond to the sender.")
					else:	
						self.client = client.TELNET(config['host'], config['port'], config['command'])
						self.log("Ssh protocol calibrated for the response.")

		elif protocol == "HTTP":
			if not self.isSupported('HTTP'):
				self.log("Error: The requested (Http) protocol is not in this component capabilities. Please fix this.")
			else:
				senderCapability = {}
				for capabil in self.status['mapping']['distribution']:
					if capabil['component'] == request['component']:
						senderCapability = capabil
						break
				#We will suppose here that a sender capability should contain the protocol it has.
				if len(senderCapability) == 0:
					self.log("Error: The communicating component is not mapped in my knowledge.")
				else:
					config = {}
					for proto in capabil['capabilities']:
						if proto['protocol'] == "HTTP":
							config = proto
							break
					if len(config) == 0:
						# print "Error: The requested protocol is not mapped. We cannot respond to the sender."
						self.log("Error: The requested protocol is not mapped. We cannot respond to the sender.")
					else:	
						self.client = client.HTTP(location="http://"+config['host']+":"+str(config['port']), endpoint=config['endpoint'])
						self.log("Tcp protocol calibrated for the response.")
		elif protocol == "BLUETOOTH":
			#Not yet implemented.
			print "Not yet implemented."
		elif protocol == "IR":
			#Not yet implemented.
			print "Not yet implemented."
		elif protocol == "I2C":
			#Not yet implemented.
			print "Not yet implemented."
		else:
			#Not supported protocol
			print "Not supported protocol"

	def process(self):
		action = self.request['message']['head']
		resolver = {}
		found = False
		for key, category in self.actions.iteritems():
			resolvers = category['resolver']
			for resol in resolvers:
				if resol['action'] == action:
					resolver = resol
					found = True
					break
			if found:
				break
		try:
			if resolver['executor'] == "bin":
				self.result = subprocess.check_output(resolver['process']+" \""+str(self.request['message']['data'])+"\"", shell=True)
			else:
				self.result = subprocess.check_output(resolver['executor']+" "+resolver['process']+"  \""+str(self.request['message']['data'])+"\"", shell=True)
		except:
			self.log("Error: Action could not be resolved.")
			self.result = ""

		if self.result == "":
			self.result = "None"
		self.log("Processed Result: "+self.result+".")

	def deliver(self):
		if self.client == None:
			self.log("Error: No chanel to respond through.")
		else:
			self.client.process(self.result)
			self.log("Result delivered to the sending component.")






