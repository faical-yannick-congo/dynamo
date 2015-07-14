import os
import sys
from parser import ParserEngine
from syntax import SyntaxEngine
from sementic import SementicEngine



if __name__ == "__main__":
	if len(sys.argv) == 0:
		print "ParserError: No file refered."
	else:
		for source_name in sys.argv[1:len(sys.argv)]:
			with open (source_name, "r") as source_file:
				source_content = source_file.read()
				print "ParserInfo: parsing source file: %s."%source_name
				parserE = ParserEngine(source_content)
				validated = parserE.parse()
				if validated:
					print "CompilerInfo: Source code is parsed with success. :-)"
					syntaxE = SyntaxEngine(source_content)
					valid = syntaxE.process()
					if valid:
						print "CompilerInfo: Source code is syntaxically correct. :-)"
						sementicE = SementicEngine(source_content, syntaxE)
						print "Collaborations: "+str(syntaxE.relationship)
						print "Roles: "+str(syntaxE.implication)
						print "Requirement: "+str(syntaxE.requirement)
						print "TR <act>: "+str(sementicE.TR("act"))
						print "PR <assign>: "+str(sementicE.PR("assign"))
						print "Tc Doctor: "+str(sementicE.Tc("Doctor"))



