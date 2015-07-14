
class SyntaxEngine:
	def __init__(self, source):
		self.source = source.replace(' ','').replace('\t','')
		self.relationship = {}
		self.implication = {}
		self.requirement = {}
		self.error = ""

	def process(self):
		cycled = self.sanity_collaborators()
		invalid = self.sanity_roles()
		unconditional = self.find_unconditionality()
		self.gen_requirement()
		return (not cycled and not invalid and not unconditional)

	def sanity_collaborators(self):
		lines = self.source.split()
		for line in lines:
			# print "Line [%d]: %s."%(line_count, line)
			step1 = line.replace("<", "< ").replace(">"," >")
			step2 = step1.split()
			if (len(step2) != 0) and ("=" in step1):
				if ("<" in step2[0]) and (">" in step2[2]):
					self.relationship[step2[1]] = {}

				index = 3
				counter = 0
				for word in step2[3:len(step2)-1]:
					if ("<" in step2[index-1]) and (">" in step2[index+1]):
						self.relationship[step2[1]][counter] = step2[index]
						counter += 1
					index += 1

		# print "Relationships: "+str(self.relationship)
		cycled = self.find_cycles()
		if cycled:
			print self.error
		return cycled

	def sanity_roles(self):
		lines = self.source.split()
		for line in lines:
			block = line.split("=")
			step1 = block[1].replace("<", " <").replace("}","} ").replace("else","").replace(";w","").replace(";s","").replace("*w","").replace("*s","").replace("|>","").replace("||","").replace("[]","")
			step2 = step1.split()
			if len(step2) != 0:
				for step3 in step2:
					if ">{" in step3:
						step4 = step3.split(">{")
						action = step4[0][1:len(step4[0])]
						roles = step4[1][0:len(step4[1])-1].split(",")
						counter = 0
						self.implication[action] = {}
						for role in roles:
							self.implication[action][counter] = role
							counter += 1
					else:
						if len(step3[1:len(step3)-1]) != 0:
							self.implication[step3[1:len(step3)-1]] = {}
		# print "Roles: "+str(self.implication)
		invalid = self.find_invalidity()
		if invalid:
			print self.error
		return invalid

	def gen_requirement(self):
		lines = self.source.split()
		flex = {}
		for line in lines:
			block = line.split("=")
			flex[block[0]] = block[1]
		for col1, value1 in flex.iteritems():
			for col2, value2 in flex.iteritems():
				flex[col2] = flex[col2].replace(col1, "("+value1+")")
		self.requirement['system'] = "Unknown"
		self.requirement['expression'] = ""
		for col, value in flex.iteritems():
			if len(self.requirement['expression']) < len(value):
				self.requirement['system'] = col
				self.requirement['expression'] = value
		# print str(self.requirement)



	def find_cycles(self):
		cycled = False
		for col1, cols1 in self.relationship.iteritems():
			for col2, cols2 in self.relationship.iteritems():
				if col1 != col2:
					if col2 in str(cols1) and col1 in str(cols2):
						cycled = True
						self.error += "SyntaxError: The collaborations %s and %s are creating a cycle.\n"%(col1, col2)
		return cycled

	def find_invalidity(self):
		invalid = False
		for action, roles in self.implication.iteritems():
			if (action != "epsilon") and (len(roles) == 0):
				invalid = True
				self.error += "SyntaxError: Fix action \'%s\', epsilon is the only core action allowed without any role.\n"%action

			for index, role in roles.iteritems():
				stak = role.split(":")
				if len(stak) == 3:
					if stak[0] != 's':
						invalid = True
						self.error += "SyntaxError: For action %s, Only the character \'s\' is authorized before \':\'.\n"%(action)
					if stak[2] != 't':
						invalid = True
						self.error += "SyntaxError: For action %s, Only the character \'t\' is authorized after \':\'.\n"%(action)
				if len(stak) == 2:
					if stak[0] == 's':
						#Good
						pass
					elif stak[1] == 't':
						#Good
						pass
					else:
						invalid = True
						self.error += "SyntaxError: For action %s, Only the character \'s\' is authorized before \':\'.\n"%(action)
						self.error += "SyntaxError: For action %s, Only the character \'t\' is authorized after \':\'.\n"%(action)
		return invalid

	def find_unconditionality(self):
		lines = self.source.split()
		line_count = 1
		unconditional = False
		for line in lines:
			begin = line.count("|>")
			end = line.count("else")
			if begin != end:
				# print "Begin %d and End %d"%(begin, end)
				unconditional = True
				self.error += "Line %d --- SyntaxError: The condition \'|> * else\' is not well written.\n"%(line_count)
			line_count += 1
		if unconditional:
			print self.error
		return unconditional



