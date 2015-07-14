
class SementicEngine:
	def __init__(self, source, syntax):
		self.syntax = syntax
		self.source = source

	def SR(self, action):
		roles = self.syntax.implication[action]
		startings = []
		for index, role in roles.iteritems():
			if "s:" in role:
				container = role.replace("s:","").replace(":t","")
				startings.append(container)
		return startings
	def TR(self, action):
		roles = self.syntax.implication[action]
		terminatings = []
		for index, role in roles.iteritems():
			if ":t" in role:
				container = role.replace("s:","").replace(":t","")
				terminatings.append(container)
		return terminatings
	def PR(self, action):
		roles = self.syntax.implication[action]
		participatings = []
		for index, role in roles.iteritems():
			if ("s:" not in role) and (":t" not in role):
				participatings.append(role)
		return participatings

	def Tc(self, composant, collaboration=None):
		if collaboration == None:
			if composant in self.syntax.requirement['expression']:
				return "Exist!"
			else:
				return None
		else:
			#Recursivity
			if "(" in collaboration:
				pass
				#Determine the operator
				#Make union or intersection.

