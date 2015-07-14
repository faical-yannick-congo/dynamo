import glob
import datetime
import time
import json
import os
from pprint import pprint
import datetime
import sys


def jsonReader(filename):
	json_data=open(filename)
	data = json.load(json_data)
	#pprint(data)
	json_data.close()
	return data


if __name__ == "__main__":
	# print "Data: "+sys.argv[1].replace("u","").replace("\'","\"")
	config = json.loads(sys.argv[1].replace("u","").replace("\'","\""))
	#Do something