import glob
import datetime
import time
import json
import os
from pprint import pprint
from processor import *
import subprocess

class CoreEngine:
	def __init__(self):
		self.last = ""
		self.stamp = ""
		self.processed = []
		self.status = {}
		self.actions = {}
		self.log_txt = "../status/log.txt"
		self.log("", 9999)
		self.reload()
		self.capabilities = []
		self.open_capabilities()
		self.log("Capabilities: "+str(self.capabilities))

	def reload(self):
		self.load_status()
		self.load_actions()


	def isCoreAction(self, action):
		if action == "sleep" or action == "wake" or action == "update" or action == "destroy":
			return True
		else:
			return False

	def open_capabilities(self):
		config = self.status['capability']['capabilities']
		for capa in config:
			try:
				server = "../listen/"+capa['protocol'].lower()+"/server.py "
				self.log("Server: "+server)
				if capa['protocol'] == "SERIAL":
					command = "python %s %s %d %d &"%(server, capa['location'], capa['baud'], capa['timeout'])
					# self.log("Command: "+command)
					pid = os.system(command)
					self.capabilities.append(pid)
					self.log("Capability ["+capa['protocol']+"] activated.")
				elif capa['protocol'] == "TCP":
					# self.log("Capability: "+str(capa))
					command = "python %s %s %d &"%(server, capa['host'], capa['port'])
					# self.log("Command: "+command)
					pid = os.system(command)
					self.capabilities.append(pid)
					self.log("Capability ["+capa['protocol']+"] activated.")
				elif capa['protocol'] == "UDP":
					# self.log("Capability: "+str(capa))
					command = "python %s %s %d &"%(server, capa['host'], capa['port'])
					# self.log("Command: "+command)
					pid = os.system(command)
					self.capabilities.append(pid)
					self.log("Capability ["+capa['protocol']+"] activated.")
				elif capa['protocol'] == "TELNET":
					command = "python %s --host %s --port %d &"%(server, capa['host'], capa['port'])
					# self.log("Command: "+command)
					pid = os.system(command)
					self.capabilities.append(pid)
					self.log("Capability ["+capa['protocol']+"] activated.")
				elif capa['protocol'] == "SSH":
					command = "python %s --host %s --ssh %d &"%(server.replace("ssh","telnet"), capa['host'], capa['port'])
					# self.log("Command: "+command)
					pid = os.system(command)
					self.capabilities.append(pid)
					self.log("Capability ["+capa['protocol']+"] activated.")
				elif capa['protocol'] == "HTTP":
					command = "python %s %s %d &"%(server, capa['host'], capa['port'])
					# self.log("Command: "+command)
					pid = os.system(command)
					self.capabilities.append(pid)
					self.log("Capability ["+capa['protocol']+"] activated.")
				else:
					self.log("Unsuported: Capability["+capa['protocol']+"] not yet supported.")
			except:
				self.log("Error: Unable to open capability["+capa['protocol']+"].")


	def load_status(self):

		self.status['behavior'] = self.jsonReader("../status/behavior.json")
		self.log("Component behavior loaded.")
		# self.log("Loading component history....")
		self.status['history'] = self.jsonReader("../status/history.json")
		self.log("Component history loaded.")
		# self.log("Loading mapping history....")
		self.status['mapping'] = self.jsonReader("../status/mapping.json")
		self.log("Component mapping loaded.")
		# self.log("Loading state history....")
		self.status['state'] = self.jsonReader("../status/state.json")
		self.log("Component state loaded.")

		self.status['capability'] = self.jsonReader("../status/capability.json")
		self.log("Component capability loaded.")

		self.dumpJson(self.status['behavior'])
		self.dumpJson(self.status['history'])
		self.dumpJson(self.status['mapping'])
		self.dumpJson(self.status['state'])
		self.dumpJson(self.status['capability'])

	def checkup(self):
		if str(self.status['behavior']) != str(self.jsonReader("../status/behavior.json")):
			self.status['behavior'] = self.jsonReader("../status/behavior.json")
			self.log("Component behavior reloaded.")
		# self.log("Loading component history....")
		if str(self.status['history']) != str(self.jsonReader("../status/history.json")):
			self.status['history'] = self.jsonReader("../status/history.json")
			self.log("Component history reloaded.")
		# self.log("Loading mapping history....")
		if str(self.status['mapping']) != str(self.jsonReader("../status/mapping.json")):
			self.status['mapping'] = self.jsonReader("../status/mapping.json")
			self.log("Component mapping reloaded.")
		# self.log("Loading state history....")
		if str(self.status['state']) != str(self.jsonReader("../status/state.json")):
			self.status['state'] = self.jsonReader("../status/state.json")
			self.log("Component state reloaded.")

		if str(self.status['capability']) != str(self.jsonReader("../status/capability.json")):
			self.status['capability'] = self.jsonReader("../status/capability.json")
			self.log("Component capability reloaded.")

		if str(self.actions['core']) != str(self.jsonReader("../actions/core/mapping.json")):
			self.actions['core'] = self.jsonReader("../actions/core/mapping.json")
			self.log("Core actions mapping reloaded.")
		if str(self.actions['custom']) != str(self.jsonReader("../actions/custom/mapping.json")):	
			self.actions['custom'] = self.jsonReader("../actions/custom/mapping.json")
			self.log("Custom actions mapping reloaded.")



	def load_actions(self):
		self.actions['core'] = self.jsonReader("../actions/core/mapping.json")
		self.log("Core actions mapping loaded.")
		self.actions['custom'] = self.jsonReader("../actions/custom/mapping.json")
		self.log("Custom actions mapping loaded.")

		self.dumpJson(self.actions['core'])
		self.dumpJson(self.actions['custom'])

	def dumpJson(self, data):
		self.log("Dump Begin----", 1)
		self.log(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')), 1)
		self.log("----Dump End", 1)

	def log(self, trace, level=0):
		if level == 9999:
			print FAIL+BOLD+"\n\n[GeneratedComponent] "+UNDERLINE+WARNING+str(datetime.datetime.now())+ENDC+OKGREEN+" ---"+" Component loading..."+ENDC
			log_file = open(self.log_txt, 'a')
			log_file.write("\n\n[GeneratedComponent] "+str(datetime.datetime.now())+" --- Component loading...")
			log_file.close()
		else:
			print FAIL+BOLD+"[GeneratedComponent] "+UNDERLINE+WARNING+str(datetime.datetime.now())+ENDC+OKGREEN+" --- " + trace+ENDC
		if level == 0:
			log_file = open(self.log_txt, 'a')
			log_file.write("\n[GeneratedComponent] "+str(datetime.datetime.now())+" --- " + trace)
			log_file.close()

	def close(self):
		self.log_txt.close()

	def extract_date(self, text):
		try:
			return datetime.datetime.strptime(text, "%Y%m%d%H%M%S%f")
		except ValueError:
			return None

	def jsonReader(self, filename):
		json_data=open(filename)
		data = json.load(json_data)
		# pprint(data)
		json_data.close()
		return data

	def process(self, filename):
		data = self.jsonReader(filename)
		if data['status'] == "processed":
			return None
		else:
			return data

	def intersect(self, a, b):
		xa = [i for i in set(a) if i not in b]
		xb = [i for i in set(b) if i not in a]
		return xa + xb

	def run(self):
		print "Started."
		while(True):
			self.checkup()
			if self.status['state']['consistency'] == "UPDATE":
				self.checkup()#Maybe put a specific update here for the actions, behavior, later.
				self.status['state']['consistency'] = "UPDATED"
				with open("../status/state.json","w") as status_file:
						status_file.write(json.dumps(self.status['state'], sort_keys=True, indent=4, separators=(',', ': ')))
			if self.status['state']['status'] == "WAKE":
				self.stamp = str(datetime.datetime.now())
				self.log("Cycle Stamp Begin: "+self.stamp+".", 1)
				requests = [req[12:len(req)-8] for req in glob.glob("../requests/*.request")]
				self.log("Requests: "+str(requests)+".", 1)
				# requests.sort(key=self.extract_date)
				filtered = self.intersect(requests, self.processed)
				filtered.sort(key=self.extract_date)
				self.log("Filtered: "+str(filtered)+".", 1)
				for request in filtered:
					self.checkup()
					if self.status['state']['consistency'] == "UPDATE":
						self.checkup()#Maybe put a specific update here for the actions, behavior, later.
						self.status['state']['consistency'] = "UPDATED"
						with open("../status/state.json","w") as status_file:
								status_file.write(json.dumps(self.status['state'], sort_keys=True, indent=4, separators=(',', ': ')))
					if self.status['state']['status'] == "WAKE":
						self.stamp = str(datetime.datetime.now())
						self.log("Cycle Stamp Process: "+self.stamp+".", 1)
						data = self.process("../requests/"+request+".request")
						if data == None:
							self.processed.append(request)
						else:
							self.log("New request ["+request+"] to process:\n"+json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))+".")
							#Process the request here.
							executor = Processor(self.stamp, self.log_txt, data, self.status, self.actions)
							executor.process()
							time.sleep(10)
							executor.deliver()
							data['status'] = "processed" #Only if the processing is finalized.
							with open("../requests/"+request+".request","w") as request_file:
								request_file.write(json.dumps(data, sort_keys=True, indent=4, separators=(',', ': ')))
							self.processed.append(request)
							self.last = request
						self.stamp = str(datetime.datetime.now())
						self.log("Cycle Stamp Processed: "+self.stamp+".", 1)
					elif self.status['state']['status'] == "SLEEP":
						time.sleep(30)
					elif self.status['state']['status'] == "DESTROY":
						break
				self.stamp = str(datetime.datetime.now())
				self.log("Cycle Stamp End: "+self.stamp+".", 1)
				time.sleep(60)#Wait 1 minute before next cycle.
			elif self.status['state']['status'] == "SLEEP":
				time.sleep(30)
			elif self.status['state']['status'] == "DESTROY":
				break






