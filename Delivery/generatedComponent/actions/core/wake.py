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
	pprint(data)
	json_data.close()
	return data


if __name__ == "__main__":
	config = json.loads(sys.argv[1].replace("u","").replace("\'","\""))
	status = jsonReader("../status/state.json")
	if config['time'] == "now":
		status['status'] = "WAKE"
	else:
		time.sleep(int(config['time']))
		status['status'] = "WAKE"
	with open("../status/state.json","w") as status_file:
		status_file.write(json.dumps(status, sort_keys=True, indent=4, separators=(',', ': ')))