
class ParserEngine:
	def __init__(self, source):
		self.source = source.replace(' ','').replace('\t','')
		self.error = ""
		# print "ParserInfo: Source..."
		# print self.source

	def parse(self):
		scoped = self.parse_scopes()
		operated = self.parse_operator()
		validated = scoped and operated
		if not validated:
			print self.error

		return validated

	def parse_scopes(self):
		paren_count = 0
		brach_count = 0
		colla_count = 0
		squar_count = 0
		verti_count = 0
		new_line = True
		line_count = 1
		character_count = 1

		for i , c in enumerate(self.source):
			if c == '=':
				if new_line:
					new_line = False
				else:
					self.error += "Line %d --- ParserError: Symbol \'=\'is forbidden twice on the same line.\n"%(line_count)
					return False
			if c == '\n':
				new_line = True
				line_count += 1
				character_count = 1
			if c == '(':
				paren_count += 1
			if c == ')':
				paren_count -= 1
			if c == '{':
				brach_count += 1
			if c == '}':
				brach_count -= 1
			if c == '<':
				colla_count += 1
			if c == '>':
				if self.source[i-1] != '|':
					colla_count -= 1
			if c == '[':
				squar_count += 1
			if c == ']':
				squar_count -= 1
			if c == '|':
				verti_count += 1
				if self.source[i-1] == '|':
					verti_count -= 1
			if c == '>':
				if self.source[i-1] == '|':
					verti_count -= 1

			character_count += 1

		if paren_count != 0:
			self.error += "ParserError: Source code should have a even number of symbol \'()\'.\n"
		if brach_count != 0:
			self.error += "ParserError: Source code should have a even number of symbol \'{}\'.\n"
		if colla_count != 0:
			self.error += "ParserError: Source code should have a even number of symbol only for collaborations \'<>\'.\n"
		if squar_count != 0:
			self.error += "ParserError: Source code should have a even number of symbol \'[]\'\n"
		if squar_count != 0:
			self.error += "ParserError: Source code should have a even number of symbol \'[]\'\n"
		if verti_count != 0:
			self.error += "ParserError: Source code should have a even number of symbol \'||\'\n"

		return (paren_count == 0) and (brach_count == 0) and (colla_count == 0) and (squar_count ==0) and (verti_count ==0)



	def parse_operator(self):
		line_count = 1
		character_count = 1

		for i , c in enumerate(self.source):
			if c == '\n':
				line_count += 1
				character_count = 1
			if c == '*':
				if i == 0:
					self.error += "Line %d --- ParserError: No operator at the begining.\n"%(line_count)
					return False
				else:
					if self.source[i+1] == 'w' or self.source[i+1] == 's':
						if self.check(i-1, i+2):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False
					else:
						self.error += "Line %d --- ParserError: Operator * need a specifier \'s\' or \'w\'.\n"%(line_count)
						return False

			if c == ';':
				if i == 0:
					self.error += "Line %d --- ParserError: No operator at the begining.\n"%(line_count)
					return False
				else:
					if self.source[i+1] == 'w' or self.source[i+1] == 's':
						if self.check(i-1, i+2):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False
					else:
						self.error += "Line %d --- ParserError: Operator ; need a specifier \'s\' or \'w\'.\n"%(line_count)
						return False
			if c == '|':
				if i == 0:
					self.error += "Line %d --- ParserError: No operator at the begining.\n"%(line_count)
					return False
				else:
					if self.source[i-1] == '|':
						# Operator ||. check now for -2 and +1
						if self.check(i-2, i+1):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False

					elif self.source[i+1] == '>':
						# Operator |>. check now for -2 and +1
						if self.check(i-1, i+2):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False
					elif self.source[i+1] == '|':
						# Operator ||. check for -1 and +2
						if self.check(i-1, i+2):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False
					else:
						self.error += "Line %d --- ParserError: reserved symbol \'|\'.\n"%(line_count)
						return False
			if c == '[':
				if i == 0:
					self.error += "Line %d --- ParserError: reserved symbol \'[\'.\n"%(line_count)
					return False
				else:
					if self.source[i+1] == ']':
						if self.check(i-1, i+2):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False
					else:
						self.error += "Line %d --- ParserError: reserved symbol \'[\'.\n"%(line_count, character_count-1)
						return False
			if c == ']':
				if i == 0:
					self.error += "Line %d --- ParserError: reserved symbol \']\'.\n"%(line_count)
					return False
				else:
					if self.source[i-1] == '[':
						if self.check(i-2, i+1):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False
					else:
						self.error += "Line %d --- ParserError: reserved symbol \']\'.\n"%(line_count, character_count-1)
						return False
			if c == 'e':
				if self.source[i:i+4] == "else":
					if i == 0:
						self.error += "Line %d --- ParserError: No operator at the begining.\n"%(line_count)
						return False
					else:
						if self.check(i-1, i+4):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False
			if c == '>':
				if i == 0:
					self.error += "Line %d --- ParserError: reserved symbol \'>\'.\n"%(line_count)
					return False
				else:
					if self.source[i-1] == '|':
						if self.check(i-2, i+1):
							#Good
							pass
						else:
							self.error += "Line %d --- ParserError: Operator should be surrounded by symbols \'<\' \'>\'.\n"%(line_count)
							return False

			character_count += 1

		return True


	def check(self, left, right):
		return (self.source[left] == '>' and self.source[right] == '<') or (self.source[left] == '}' and self.source[right] == '<') or (self.source[left] == ')' and self.source[right] == '<') or (self.source[left] == ')' and self.source[right] == '(' or (self.source[left] == '}' and self.source[right] == '(') or (self.source[left] == '>' and self.source[right] == '('))