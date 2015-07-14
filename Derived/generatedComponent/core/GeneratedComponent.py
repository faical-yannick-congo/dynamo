import sys
import os.path

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import json
from core import CoreEngine

mode = 0 # 1=debug and 2=real

if __name__ == "__main__":
	params = sys.argv
	coreEngine = CoreEngine()
	coreEngine.run()

	if params[1] == "--debug":
		mode = 1
		#Open log.txt in write mode
		#Load status mapping
		#Load behavior
		#Load actions core mapping
		#Load actions custom mapping
		#display the last history (requirement)


		#update state.
	elif params[1] == "--real":
		mode = 2
		#Load actions core mapping
		#Load actions custom mapping
	else:
		print "Execution mode unrecognized. Default will be taken."